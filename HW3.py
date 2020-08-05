import pandas as pd


#Q1
gold = pd.read_csv("C:/Users/timot/Downloads/gold.txt", sep = "\t", names = ["url","rating"])
labels = pd.read_csv("C:/Users/timot/Downloads/labels.txt", sep = "\t",names = ["turk","url","rating"])

#Q2

#labels = labels.drop_duplicates()
labels_on_gold = gold.merge(labels, on = "url")

def masked(s):
    return s not in labels_on_gold["url"].values

mask = labels["url"].map(masked)
labels_unknown = labels[mask]


#Q3

turk = []
total = []
accuracy = []

groups = labels_on_gold.groupby("turk")

for name, info in groups:
    right = 0
    turk.append(name)
    tot = len(info["url"])
    total.append(tot)
    for i in range(tot):
        if info["rating_x"].iloc[i] == info["rating_y"].iloc[i]:
            right += 1
    accurate = right/tot
    accuracy.append(accurate)
    
data = {"total": total, "accuracy": accuracy}
    
rater_goodness = pd.DataFrame(data,index = turk)

#Q4

rater_goodness["odds"] = rater_goodness["accuracy"]/(1.001 - rater_goodness["accuracy"])

#Q5

mask = (rater_goodness["total"] >= 20)
topraters = rater_goodness[mask]
topraters.iloc[:20]

#Q6
mask = (rater_goodness["total"] < 20)
botraters = rater_goodness[mask]

topraters.iloc[:40]
botraters.iloc[:20]


# In generaly yes.  People who have more ratings have generally >50% average correctness. (There are exceptions) 

#Q7

mask1 = (rater_goodness["total"] > 1)
firstset = rater_goodness[mask1].sort_values(by = "total", ascending = False)
top = round(0.25*269)
topset = firstset.iloc[:top]

turks = topset.index
allturks = labels_unknown["turk"].values

def cutout(s):
    return s in turks

mask = labels_unknown["turk"].map(cutout)
reliable1 = labels_unknown[mask]

# Add back turk to merge
rater_goodness["turk"] = rater_goodness.index

full = reliable1.merge(rater_goodness,on = "turk",how = "left",validate = "many_to_one")


reliable = full[["turk","url","rating","odds"]]

def product(x):
    tot = 1
    for i in x:
        tot *= i
    return tot

table = pd.pivot_table(reliable,index = 'url',columns = 'rating',values = 'odds',aggfunc = product,fill_value = 0)

#Q8
overall= []
category = []
for i in range(len(table)):
    big = max(table.iloc[i])
    overall.append(big)
    rating = table.iloc[i].idxmax(axis = 1)
    category.append(rating)
    
data1 = {"top category":category, "top odds":overall}
result_75 = pd.DataFrame(data1,index = table.index)


#Q9 
# same as Q7 but with different quartile

top = round(0.75*269)
topset = firstset.iloc[:top]

turks = topset.index
allturks = labels_unknown["turk"].values

def cutout(s):
    return s in turks

mask = labels_unknown["turk"].map(cutout)
reliable1 = labels_unknown[mask]

# Add back turk to merge

full = reliable1.merge(rater_goodness,on = "turk",how = "left",validate = "many_to_one")


reliable = full[["turk","url","rating","odds"]]

table = pd.pivot_table(reliable,index = 'url',columns = 'rating',values = 'odds',aggfunc = product,fill_value = 0)

overall= []
category = []
for i in range(len(table)):
    big = max(table.iloc[i])
    overall.append(big)
    rating = table.iloc[i].idxmax(axis = 1)
    category.append(rating)
    
data1 = {"top category":category, "top odds":overall}
result_25 = pd.DataFrame(data1,index = table.index)

#make copies just in case
copy1 = result_75.copy()
copy1["urls"] = copy1.index
copy2 = result_25.copy()
copy2["urls"] = copy2.index

total = copy1.merge(copy2,on = "urls",how = "left")
total.columns = ["reliable","1","x","less reliable","4"]

subset = total[["reliable","less reliable"]]
subset["counts"] = 1

table2 = pd.pivot_table(subset,index = "reliable",columns = "less reliable", values = "counts", aggfunc = sum)

# Most errors are when the reliable set rates G and unreliable rates P


