import numpy as np
import xml.dom.minidom
import time
import copy
import xmlParse as xp
import  bifParse as bp


def P_child_parent(child, evidences):
    # child of definition
    global definition
    for def_child in definition:
        # find the child with the name
        childName = def_child.getElementsByTagName('FOR')[0].firstChild.data
        if childName == list(child.keys())[0]:
            # generate the parent string for finding the value
            parent_str = ''
            if len(def_child.getElementsByTagName('GIVEN')) == 0:
                value_list = def_child.getElementsByTagName('TABLE')[0].firstChild.data.split()
                if list(child.values())[0]:
                    return value_list[0]
                else:
                    return value_list[1]
            for given in def_child.getElementsByTagName('GIVEN'):
                if given.firstChild.data in evidences.keys():
                    if evidences[given.firstChild.data]:
                        parent_str += ' ' + given.firstChild.data
                    else:
                        parent_str += ' !' + given.firstChild.data
            # get the correct row of table
            child_lenth = len(def_child.getElementsByTagName('TABLE')[0].childNodes)
            for i in range(child_lenth):
                table_row = def_child.getElementsByTagName('TABLE')[0].childNodes[i]
                if parent_str in table_row.data:
                    value_list = def_child.getElementsByTagName('TABLE')[0].childNodes[i+1].data.split()
                    if list(child.values())[0]:
                        return value_list[0]
                    else:
                        return value_list[1]


# return the children list of given parentNode
def childCheck(parentNode):
    global var_parent
    children = []
    for var in list(var_parent.keys()):
        if parentNode in var_parent[var]:
            children.append(var)
    return children




def Gibbs_Sample(z, child_list, x):
    result = []
    for z_value in get_var_domain(z):
        x[z] = z_value
        p = float(get_value_out(z, z_value, x))
        for child in child_list:
            p *= float(get_value_out(child, x[child], x))
        result.append(p)
    return result



def Gibbs_Ask(X, e, bn_VARS, N):
    Z = []
    x_dic = {}
    X_domain = get_var_domain(X)
    W = [0]*len(X_domain)
    for var in bn_VARS:
        if var not in list(e.keys()):
            # not evidence then add to Z list and initial a value
            Z.append(var)
            randValue = np.random.randint(0,len(get_var_domain(var)))
            x_dic[var] = get_var_domain(var)[randValue]
        else:
            # evidence then add to x dictionary
            x_dic[var] = e[var]
    for j in range(N):
        for z in Z:
            childList = childCheck(z)
            result = Gibbs_Sample(z, childList, x_dic)
            result = normalize(result)
            x_dic[z] = get_var_domain(z)[random(result)]
            # check the state of X
            for i in range(len(X_domain)):
                if X_domain[i] == x_dic[X]:
                    W[i] += 1
    print(W)
    return(W)



# Random function
def random(p_list):
    rand_p = np.random.uniform(0,1)
    list_sum = 0
    for i in range(len(p_list)):
        list_sum += float(p_list[i])
        if rand_p <= list_sum:
            return i


# Normalize
def normalize(list):
    new_list = []
    for i in list:
        new_list.append(float(i/float(sum(list))))
    return new_list



# get variable's domain into a list
def get_var_domain(var):
    global var_domain
    return var_domain[var]


# get variable's parent list
def get_var_parents(var):
    global var_parent
    return(var_parent[var])


# generate a tuple in parents' order
def gen_parent_string(var, evidence):
    parent_tuple = ()
    parent = get_var_parents(var)
    if len(parent)!=0:
        for p in parent:
            parent_tuple += (str(evidence[p]).upper(),)
    return parent_tuple

# get the value list of given variable and evidences
def get_value_list(var, evidence):
    parent_tuple = gen_parent_string(var, evidence)
    global prob_dict
    value_list = prob_dict[var][parent_tuple]
    return value_list


# get exact value for a domain of var
def get_value_out(var, var_value, evidence):
    value_list = get_value_list(var, evidence)
    domain_list = get_var_domain(var)
    for i in range(len(domain_list)):
        if domain_list[i].lower() == str(var_value).lower():
            return value_list[i]








def get_right_order(var_parent):
    n = 0
    name_list = []
    while len(var_parent) > 0:
        n += 1
        #print(var_parent)
        if n%2 == 1:
            var_parent_copy = copy.deepcopy(var_parent)
            for var in list(var_parent_copy.keys()):
                if len(var_parent_copy[var]) == 0:
                    var_parent.pop(var)
                    name_list.append(var)
        else:
            var_parent_copy = copy.deepcopy(var_parent)
            for var in list(var_parent_copy.keys()):
                for parent in var_parent_copy[var]:
                    if parent in name_list:
                        var_parent[var].remove(parent)
    return name_list



def main(N, X, e):
    '''
    global definition
    dom = xml.dom.minidom.parse(xml_file)
    root = dom.documentElement
    definition = root.getElementsByTagName('DEFINITION')

    bn_VARS = []
    variables = root.getElementsByTagName('VARIABLE')
    '''
    global name_list
    bn_VARS = name_list
    value = Gibbs_Ask(X, e, bn_VARS, N)
    value = normalize(value)  # normalize
    result_dict = {}
    X_domain = get_var_domain(X)
    for i in range(len(X_domain)):
        result_dict[X_domain[i]] = value[i]
    return (result_dict)



def test_ins():
    while True:
        '''
        # N, file_name, X, e = input('Please type in the instructions to test: ')
        file_name = 'insurance.bif'
        #file_name = 'dog-problem.xml'
        X = 'HISTORY'
        #X = 'family-out'
        e = {'PULMEMBOLUS': False}
        #e = {'bowel-problem': 'true'}
        N = 1000
        # read file data into dictionaries
        '''
        # 1000, 'alarm.bif', 'HISTORY', {'PULMEMBOLUS': False}
        # 1000, 'insurance.bif', 'GoodStudent', {'Age': 'Adult', 'Mileage': 'FiveThou'}
        # 1000, 'diabetes.bif', 'meal_0', {'bg_8':'v20mmol_l'}
        # 1000, 'dog-problem.xml', 'family-out', {'bowel-problem': 'true'}
        #N = 1000
        #file_name = 'i'
        N, file_name, X, e = 1000, 'alarm.bif', 'HISTORY', {'PULMEMBOLUS': False, 'Mileage': 'FiveThou'}
        global var_domain, prob_dict, var_parent, name_list
        if file_name[-3:] == 'bif':
            var_domain, prob_dict, var_parent, name_list = bp.parse(file_name)
            var_parent_copy = copy.deepcopy(var_parent)
            name_list = get_right_order(var_parent_copy)
            print(prob_dict)
        elif file_name[-3:] == 'xml':
            var_domain, prob_dict, var_parent, name_list = xp.parse(file_name)  # xml parser py
            var_parent_copy = copy.deepcopy(var_parent)
            name_list = get_right_order(var_parent_copy)
        tic = time.time()
        result = main(N, X, e)
        toc = time.time()
        print('The result is {0} and time spent is {1} seconds').format(result, toc - tic)

# ('aima-alarm.xml', 'B', {'J':True,'M':True}, 1000)

xml_file = 'aima-alarm.xml'
#xml_file = 'aima-wet-grass.xml'
X='B'
#X='R'
e={'J':True,'M':True}
#e={'S':True}
#print(main(10000, xml_file, X, e))
test_ins()


