
# coding: utf-8

# In[ ]:


## import modules needed
import numpy as np
import pandas as pd
import operator
import time
import matplotlib.pyplot as plt
from collections import defaultdict
from collections import OrderedDict
from itertools import chain, combinations
import random
import os


# In[ ]:


## load the data into pandas data frame
#file_path=os.path.join("data","adult.data")
file_path = 'adult.data'
data_df=pd.read_csv(file_path, sep=',', names=['age','work_class','fnlwgt','edu_degree','edu_yr','marital_status','occupation','relationship','race','sex','cpt_gain','cpt_loss','week_hour','country','category'])
data_df['age']='at '+(data_df['age']-data_df['age']%10).apply(str)
data_df['week_hour']=(data_df['week_hour']-data_df['week_hour']%10).apply(str)+'-'+(data_df['week_hour']-data_df['week_hour']%10+10).apply(str)+' hrs'
#data_df['edu_yr']='school year '+(data_df['edu_yr']).apply(str)
data_df['week_hour']='work hour '+(data_df['week_hour']).apply(str)
data_df.loc[data_df.edu_yr>8,'edu_yr']='edu_yr >8'
data_df.loc[data_df.edu_yr!='edu_yr >8','edu_yr']='edu_yr <=8'
data_df.loc[data_df.cpt_gain>0,'cpt_gain']='gain'
data_df.loc[data_df.cpt_loss>0,'cpt_loss']='loss'
data_df.loc[data_df.cpt_gain==0,'cpt_gain']='no gain'
data_df.loc[data_df.cpt_loss==0,'cpt_loss']='no loss'

## entries with earn >50K
more50K_df=data_df.loc[data_df.category==' >50K']
more50K_df=more50K_df.drop(['category','fnlwgt', 'cpt_gain','cpt_loss'],axis=1)
## entries with earn <=50K
less50K_df=data_df.loc[data_df.category==' <=50K']
less50K_df=less50K_df.drop(['category','fnlwgt', 'cpt_gain','cpt_loss'],axis=1)
##reset_index
more50K_df=more50K_df.reset_index().drop('index',axis=1)
less50K_df=less50K_df.reset_index().drop('index',axis=1)
##sample data from more50K_df
less50K_df.head()


# In[ ]:


## first let's check L1 itemset with min_sup> 10% for people earn>50K and earn<=50K
min_sup=0.3
more50K_size=len(more50K_df)
less50K_size=len(less50K_df)
L1_more50K={}
L1_less50K={}
col_names=list(more50K_df.columns.values)
for name in col_names:
    temp1=more50K_df.groupby(name).size().reset_index()
    temp2=less50K_df.groupby(name).size().reset_index()
    for index,row in temp1.iterrows():
        if float(row[0]/more50K_size)>=min_sup:
            L1_more50K[row[name]]=row[0]
    for index,row in temp2.iterrows():
        if float(row[0]/less50K_size)>=min_sup:
            L1_less50K[row[name]]=row[0]
## visualization of frequent single items in both situations
List_more50K=sorted(L1_more50K.items(),key=operator.itemgetter(1),reverse=True)
List_less50K=sorted(L1_less50K.items(),key=operator.itemgetter(1),reverse=True)
print("frequent single item with >50K annual income: \n",List_more50K,'\n') 
print("frequent single item with <=50K annual income: \n",List_less50K,'\n')
x_more50K, y_more50K=zip(*List_more50K)
x_less50K, y_less50K=zip(*List_less50K)
ind1=np.arange(len(x_more50K))
ind2=np.arange(len(x_less50K))
y_more50K=[x/more50K_size for x in y_more50K]
y_less50K=[x/less50K_size for x in y_less50K]
##plot frequent 1-item sets
f,(ax1,ax2)=plt.subplots(1,2,sharey=True)
f.set_figheight(5)
f.set_figwidth(15)
ax1.bar(ind1, y_more50K, 0.7, color='r')
ax1.set_xticks(ind1)
ax1.set_xticklabels(x_more50K,rotation=90)
ax1.set_title("frequent 1-itemsets for >50K")
ax2.bar(ind2, y_less50K, 0.7, color='b')
ax2.set_xticks(ind2)
ax2.set_xticklabels(x_less50K,rotation=90)
ax2.set_title("frequent 1-itemsets for <=50K")
plt.show()


# In[ ]:


############################################################
## Apriori algorithm
############################################################

def Apriori(data_df,min_sup, itemset_len):
    frequent_sets={}
    L1=set()
    total_size=len(data_df)
    min_cnt=int(total_size*min_sup)
    col_names=list(data_df.columns.values)
    for col_name in col_names:
        temp=data_df.groupby(col_name).size().reset_index()
        for index,row in temp.iterrows():
            if row[0]>=min_cnt:
                elem=frozenset([row[col_name]])
                L1.add(elem)
    frequent_sets[1]=L1
    for k in range(2,itemset_len+1):
        last_set=frequent_sets[k-1]
        frequent_sets[k]=gen_freq_set(data_df,min_cnt,last_set, L1)
        del frequent_sets[k-1]
    return frequent_sets[itemset_len]


def gen_freq_set(data_df, min_cnt, last_freq_set, L1_set):
    counts=defaultdict(int)
    for index,row in data_df.iterrows():
        row=set(row)
        for itemset in last_freq_set:
            if  itemset.issubset(row):
                for another_item in row-itemset:
                    another_item= frozenset([another_item])
                    #print(another_item)
                    if another_item in L1_set:
                        superset= itemset | another_item #frozenset([another_item])
                        counts[superset]+=1
                    else:
                        continue
    #counts =sorted(counts.items(), key=operator.itemgetter(1), reverse=True)
    #next_set, cnt=zip(*counts)
    #for item,count in counts:
    #    next_set.append(item)
    #print(counts)
    return frozenset([itemset for itemset, freq in counts.items() if freq>min_cnt])

###################################################################################
## FP_Tree algorithm
###################################################################################

## a class of tree nodes used in building tree###################
class treeNode:
    def __init__(self, val, val_count, parentNode):
        self.name=val
        self.count=val_count
        self.nodelink=None  ## a link to connect leafs
        self.parent=parentNode
        self.children={}
    def addCount(self, new_income):
        self.count+=new_income
    def printTree(self, blank=1):
        print("   "*blank, self.name, ' ', self.count)
        for child in self.children.values():
            child.printTree(blank+1)

## find the frequent 1-itemset
def singleFreqItem(data_df, min_cnt):
    L1={}
    total_size=len(data_df)
    col_names=list(data_df.columns.values)
    for col_name in col_names:
        temp=data_df.groupby(col_name).size().reset_index()
        for index,row in temp.iterrows():
            if row[0]>=min_cnt:
                L1[row[col_name]]=row[0]
    L1=sorted(L1.items(),key=operator.itemgetter(1),reverse=True) #return a list of tuples
    return L1

## build the tree
def build_tree(data_df, min_sup):
    min_cnt=int(len(data_df)*min_sup)
    #first find the frequent 1-itemset L1
    L1_ItemCnt=singleFreqItem(data_df,min_cnt)
    if len(L1_ItemCnt)==0:
        return
    L1_item, L1_cnt=zip(*L1_ItemCnt)
    #build the header table
    header={}
    for item in L1_item:
        header[item]=None
    #print(header)
    #now build the tree
    root=treeNode(val='NULL', val_count=0,parentNode=None)
    for index, row in data_df.iterrows():
        row=list(row)
        localSet=[]
        for item in row:
            if item in L1_item:
                localSet.append(item)
        if len(localSet)>0:
            #print(localSet)
            localSet=sorted(localSet, key=lambda x: L1_item.index(x))
            insertTree(localSet,root,header)
        #print(localSet)
    return root, header, L1_item

## insert an itemset into the FP-tree
def insertTree(localSet, node, header):
    for item in localSet:
        if item in node.children:
            node.children[item].addCount(1)
        else:
            node.children[item]=treeNode(item,1,node)
            if header[item]==None:
                header[item]=node.children[item]
            else:
                headerNode=header[item]
                while(headerNode.nodelink!=None):
                    headerNode=headerNode.nodelink
                headerNode.nodelink=node.children[item]
        node=node.children[item]


##now mining the FP-tree
def climbTree(node, prePath):
    if node.parent!=None:
        prePath.append(node.name)
        climbTree(node.parent, prePath)
        
def prefixPath(endVal, node):
    condPaths={}
    while node!=None:
        prePath=[]
        climbTree(node, prePath)
        if len(prePath)>1:
            condPaths[frozenset(prePath)]=node.count
        node=node.nodelink
    return condPaths

## final wraper
def FPTree(data_df, min_sup):
    root, header, L1=build_tree(data_df, min_sup)
    all_freq_items=[]
    for item in L1:
        if item in header:
            cur_paths=prefixPath(item, header[item])
            all_freq_items.append(cur_paths)
    return all_freq_items

##########################################################
###### Random Sampling Apriori
##########################################################

def gen_cand_set(samples, cur_len, last_freq_itemset, min_cnt, negative_border):
    counts={}
    freq_sets=set()
    for index, row in samples.iterrows():
        row=list(row)
        for item in combinations(row,cur_len):
            item=frozenset(item)
            counts.setdefault(item,0)
            counts[item]+=1
    for item in counts:
        if counts[item]>min_cnt:
            freq_sets.add(item)
        else: 
            if len(item)==1: # a single itemset, save it for checking later
                negative_border.add(item)
            else:
                break_flag=0
                for subset in combinations(item,cur_len-1):
                    if frozenset(subset) not in last_freq_itemset:
                        break_flag=1
                        break
                if break_flag==0:
                    negative_border.add(item)
    return freq_sets

def samplingApriori(data_df, min_sup, max_len, sampleSize=0.2):
    sample_min_cnt=int(sampleSize*len(data_df)*min_sup)
    min_cnt=int(len(data_df)*min_sup)
    # I just simply assume the data is randomized nicely, so only make a slice of data directly for samples
    samples= data_df.iloc[:int(sampleSize*len(data_df))]
    cand_freq_sets={}
    negative_border=set()
    # generat frequent 1-itemset
    col_names=list(data_df.columns.values)
    L1=set()
    for col_name in col_names:
        temp=data_df.groupby(col_name).size().reset_index()
        for index,row in temp.iterrows():
            if row[0]>=min_cnt:
                elem=frozenset([row[col_name]])
                L1.add(elem)
    cand_freq_sets[1]=L1 
    for i in range(2,max_len+1):
        cand_freq_sets[i]=gen_cand_set(samples,i,cand_freq_sets[i-1],sample_min_cnt,negative_border)
    counts={}
    for index, row in data_df.iterrows():
        row=frozenset(row)
        for item in negative_border:
            if frozenset(item).issubset(row):
                counts.setdefault(frozenset(item),0)
                counts[frozenset(item)]+=1
        for i in range(1,max_len+1):
            for item in cand_freq_sets[i]:
                if item.issubset(row):
                    counts.setdefault(item,0)
                    counts[item]+=1
    return [(itemset,frequent) for itemset,frequent in counts.items() if frequent>min_cnt]

## a samplingApriori without checking negative
def samplingApriori_NoNeg(data_df, min_sup, max_len, sampleSize=0.2):
    sample_min_cnt=int(sampleSize*len(data_df)*min_sup)
    min_cnt=int(len(data_df)*min_sup)
    # I just simply assume the data is randomized nicely, so only make a slice of data directly for samples
    samples= data_df.iloc[:int(sampleSize*len(data_df))]
    cand_freq_sets={}
    negative_border=set()
    # generat frequent 1-itemset
    col_names=list(data_df.columns.values)
    L1=set()
    for col_name in col_names:
        temp=data_df.groupby(col_name).size().reset_index()
        for index,row in temp.iterrows():
            if row[0]>=min_cnt:
                elem=frozenset([row[col_name]])
                L1.add(elem)
    cand_freq_sets[1]=L1 
    for i in range(2,max_len+1):
        cand_freq_sets[i]=gen_cand_set(samples,i,cand_freq_sets[i-1],sample_min_cnt,negative_border)
    counts={}
    for index, row in data_df.iterrows():
        row=frozenset(row)
        for i in range(1,max_len+1):
            for item in cand_freq_sets[i]:
                if item.issubset(row):
                    counts.setdefault(item,0)
                    counts[item]+=1
    return [(itemset,frequent) for itemset,frequent in counts.items() if frequent>min_cnt]


# In[ ]:


## time testing for all methods
## visualize the time results
supports=[0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7, 0.75, 0.8]
## all time in sec
apriori_time=[]
FP_time=[]
sampling_time=[]
for sup in supports:
    start1 = time.time()
    apr_res=Apriori(less50K_df,sup,10)
    end1 = time.time()
    print("With min support= ", sup, " Apriori Ellapse time: ", end1 - start1, " s \n")
    apriori_time.append(end1-start1)
    start2 = time.time()
    FP_res=FPTree(less50K_df, sup)
    end2 = time.time()
    print("With min support= ", sup, " FP-tree time: ", end2 - start2, " s \n")
    FP_time.append(end2-start2)
    start3 = time.time()
    sampling_res=samplingApriori(less50K_df, sup, 10)
    end3 = time.time()
    print("With min support= ", sup, " Random Sampling time: ", end3 - start3, " s \n")
    sampling_time.append(end3-start3)

## visualize the results
plt.figure(figsize=(5,5))
plt.plot(supports, apriori_time, label='Apriori')
plt.plot(supports, FP_time, label='FP Tree')
plt.plot(supports, sampling_time, label='Random Sampling')
plt.legend(loc='best')
plt.xlabel('Support Level')
plt.ylabel('Execution Time Secs')
plt.title('Execution Time for <=50K data')
plt.show()


# In[ ]:


## time testing for random sampling
## to see if the method is staple without checking negative border
supports=[0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7, 0.75, 0.8]
sampling_time=[]
sampling_NoNeg_time=[]
missing_item=[]
for sup in supports:
    start3 = time.time()
    sampling_res=samplingApriori(less50K_df, sup, 10)
    end3 = time.time()
    print("With min support= ", sup, " Random Sampling time: ", end3 - start3, " s \n")
    sampling_time.append(end3-start3)
    ## check if we don't count the nagative border
    start4 =time.time()
    sampling_NoNeg_res=samplingApriori_NoNeg(less50K_df, sup, 10)
    end4=time.time()
    print("With min support= ", sup, " Random Sampling without negative border time: ", end4 - start4, " s \n")
    print("Difference between results in itemset number",len(sampling_res)-len(sampling_NoNeg_res))
    missing_item.append(len(sampling_res)-len(sampling_NoNeg_res))

##make a plot of missing itemset number as a function of minimum support threshold
plt.figure(figsize=(5,5))
plt.plot(supports,missing_item)
plt.xlabel('Support Level')
plt.ylabel('Number of missing itemset')
plt.title('Number of missing itemset without negative border')
plt.show()


# In[ ]:


## find the association rules for >50K
## using a minimum support=0.5
min_sup=0.5
item_cnt=samplingApriori(more50K_df, min_sup, 10)
itemsets,counts=zip(*item_cnt)
total_size=len(data_df)   ##total number of transactions
rules={}

## find the total count of each candidate itemset in all transactions
total_counts={}
for index, row in data_df.iterrows():
    row=frozenset(row)
    for item in itemsets:
        if item.issubset(row):
            total_counts.setdefault(item,0)
            total_counts[item]+=1

sup_more50K=float(len(more50K_df)/len(data_df))
sup_less50K=float(len(less50K_df)/len(data_df))
## find the support of each item
for i in range(len(counts)):
    cand_item=itemsets[i]
    rules[cand_item]=[]
    support=float(counts[i]/total_size)   ## calculate the support level of the candidate itemset
    rules[cand_item].append(support)
    confidence=counts[i]/total_counts[cand_item]  ## confidence level of the candidate itemset
    lift=counts[i]/(total_counts[cand_item]*sup_more50K) ## lift level of the candidate itemset
    conviction=(1-sup_more50K)/(1-confidence)
    rules[cand_item].append(confidence)
    rules[cand_item].append(lift)
    rules[cand_item].append(conviction)
    #print("itemset: ", cand_item, " counts: ", counts[i]," support: ", support," confidence: ", confidence, " lift: ", lift, " conviction: ", conviction, "\n")
##  sort the result
sorted_rules=sorted(rules.items(), key=lambda e: e[1][1], reverse=True)
###    (itemset, support, confidence, lift, conviction)
for item in sorted_rules:
    print(item,'\n')


# In[ ]:


## find the association rules for <=50K
## using a minimum support=0.5
min_sup=0.5
item_cnt=samplingApriori(less50K_df, min_sup, 10)
itemsets,counts=zip(*item_cnt)
total_size=len(data_df)   ##total number of transactions
rules={}

## find the total count of each candidate itemset in all transactions
total_counts={}
for index, row in data_df.iterrows():
    row=frozenset(row)
    for item in itemsets:
        if item.issubset(row):
            total_counts.setdefault(item,0)
            total_counts[item]+=1

sup_more50K=float(len(more50K_df)/len(data_df))
sup_less50K=float(len(less50K_df)/len(data_df))
## find the support of each item
for i in range(len(counts)):
    cand_item=itemsets[i]
    rules[cand_item]=[]
    support=float(counts[i]/total_size)   ## calculate the support level of the candidate itemset
    rules[cand_item].append(support)
    confidence=counts[i]/total_counts[cand_item]  ## confidence level of the candidate itemset
    lift=counts[i]/(total_counts[cand_item]*sup_less50K) ## lift level of the candidate itemset
    conviction=(1-sup_less50K)/(1-confidence)
    rules[cand_item].append(confidence)
    rules[cand_item].append(lift)
    rules[cand_item].append(conviction)
    #print("itemset: ", cand_item, " counts: ", counts[i]," support: ", support," confidence: ", confidence, " lift: ", lift, " conviction: ", conviction, "\n")
    
sorted_rules=sorted(rules.items(), key=lambda e: e[1][1], reverse=True)
###    (itemset, support, confidence, lift, conviction)
for item in sorted_rules:
    print(item,'\n')


# In[ ]:


len(more50K_df)


# In[ ]:


len(less50K_df)

