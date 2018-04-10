import numpy as np

raw_data = open('adult.data')
line = raw_data.readline()
dataset = []
while line:
    if line == '':
        break
    line_data = line.strip().split(', ')
    dataset.append(line_data)
    line = raw_data.readline()

N = len(dataset)    # the number of whole data
threshold = 0.6     # set the value for threshold
freq_items = {}

# check 1-item frequency
for line in dataset:
    for item in line:
        if item in freq_items:
            freq_items[item] += 1
        else:
            freq_items[item] = 1


def prune(old):
    new = {}
    for item in old.keys():
        #print N*threshold
        if old[item] > N * threshold:
            new[item] = old[item]
    return new

new_freq_items = prune(freq_items)  # apply the prune process

''' The improved process '''
def modified_(old_freq, number):
    ele_dict = {}
    for item in old_freq.keys():
        for ele in item:
            if ele in ele_dict:
                ele_dict[ele] += 1
            else:
                ele_dict[ele] = 1

    # drop the element which show up times less than number
    drop_list = []
    for ele in ele_dict.keys():
        if ele_dict[ele] < number:
            drop_list.append(ele)

    # build the new freq dict without the dropped elements
    new_freq = {}
    for item in old_freq.keys():
        for drop_ele in drop_list:
            if drop_ele not in item:
                new_freq[item] = old_freq[item]

    # return
    return new_freq





print str(1) + '-items frequent items:'
print new_freq_items
print '\n'

#freq_items = new_freq_items # drop the former freq items, store the freq items in freq_items

#freq_list = new_freq_items.keys()   # build the freq items list

#new_freq_items = {} # initial the freq item set



number = 1
while len(new_freq_items) > 0:
    number += 1
    freq_list = new_freq_items
    new_freq_items = {}
    # generate the 2-item freq dictionary
    for i in freq_list:
        for j in freq_list:
            s = set()
            if type(i) == tuple:
                #print set(i)
                s = set(i) | set(j)
            else:
                s.add(i)
                s.add(j)
            #print s
            if len(s)==number:
                new_freq_items[tuple(s)] = 0
    # new_freq_items is the generated n-items dict

    #print new_freq_items
    # check n-item freq dict
    for line in dataset:
        for item in new_freq_items:
            if set(item).issubset(set(line)):
                new_freq_items[item] += 1

    #print new_freq_items
    # prune the freq dict
    new_freq_items = prune(new_freq_items)

    #print new_freq_items

    # show the result
    print str(number) + '-items frequent items:'
    print new_freq_items
    print '\n'

    # implement the modified algorithm
    new_freq_items = modified_(new_freq_items, number)



# correct result
# [set(['Male']), set(['0', 'Male']), set(['Private']), set(['United-States', 'Private']), set(['0', 'United-States', 'Private']), set(['0', 'Private']), set(['<=50K']), set(['<=50K', 'White']), set(['<=50K', '0', 'White']), set(['<=50K', 'United-States']), set(['<=50K', '0', 'United-States']), set(['<=50K', '0']), set(['White']), set(['White', 'United-States']), set(['0', 'White', 'United-States']), set(['0', 'White']), set(['United-States']), set(['0', 'United-States']), set(['0'])]

'''
# generate the 2-item freq dictionary
for i in freq_list:
    for j in freq_list:
        if i != j:
            new_freq_items[(i,j)] = 1

# check 2-item frequency
for line in dataset:
    for item in new_freq_items:
        if set(item).issubset(set(line)):
            new_freq_items[item] += 1

print prune(new_freq_items)
'''

