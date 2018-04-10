import numpy as np
import xml.dom.minidom
import time
import bifParse as bp
import xmlParse as xp
import copy

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





def LikeLiHood_Weighting(X, e, bn_VARS, N):
    X_domain = get_var_domain(X)
    W = [0]*len(X_domain)
    for i in range(N):
        x_dic, w = Weighted_Sample(bn_VARS, e)
        for i in range(len(X_domain)):
            if X_domain[i] == x_dic[X]:
                W[i] += w
    return(W)




def Weighted_Sample(bn, e):
    x_dic = {}
    w = 1
    for var in bn:
        if var in list(e.keys()):
            w *= float(get_value_out(var, e[var], x_dic))
            x_dic[var] = e[var]
        else:
            P_list = get_value_list(var, x_dic)
            # random(P_list)  # random function for set value
            x_dic[var] = get_var_domain(var)[random(P_list)]
    #print(x_dic, w)
    return (x_dic, w)

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


# main function
def main(N, X, e):
    '''
    global definition
    dom = xml.dom.minidom.parse(xml_file)
    root = dom.documentElement
    definition = root.getElementsByTagName('DEFINITION')

    bn_VARS = []
    variables = root.getElementsByTagName('VARIABLE')
    for variable in variables:
        bn_VARS.append(variable.getElementsByTagName('NAME')[0].firstChild.data)
    '''
    global var_domain
    global name_list
    bn_VARS = name_list # get all var in bn
    X_domain = get_var_domain(X)

    value = LikeLiHood_Weighting(X, e, bn_VARS, N)
    value = normalize(value)    # normalize
    result_dict = {}
    for i in range(len(X_domain)):
        result_dict[X_domain[i]] = value[i]
    return(result_dict)


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



def test_ins():
    while True:
        '''
        # N, file_name, X, e = input('Please type in the instructions to test: ')
        file_name = 'alarm.bif'
        #file_name = 'dog-problem.xml'
        X = 'HISTORY'
        #X='family-out'
        e = {'PULMEMBOLUS': False}
        #e={'bowel-problem':'true'}
        N = 1000
        # read file data into dictionaries
        '''
        N, file_name, X, e = input('Please type in the instructions to test: ')
        global var_domain, prob_dict, var_parent, name_list

        if file_name[-3:]=='bif':
            var_domain, prob_dict, var_parent, name_list = bp.parse(file_name)
            var_parent_copy = copy.deepcopy(var_parent)
            name_list = get_right_order(var_parent_copy)
        elif file_name[-3:]=='xml':
            var_domain, prob_dict, var_parent, name_list = xp.parse(file_name) # xml parser py
            var_parent_copy = copy.deepcopy(var_parent)
            name_list = get_right_order(var_parent_copy)
        tic = time.time()
        result = main(N, X, e)
        toc = time.time()
        print('The result is {0} and time spent is {1} seconds').format(result, toc - tic)


xml_file = 'aima-alarm.xml'
#xml_file = 'aima-wet-grass.xml'
X='B'
#X='R'
e={'J':True,'M':True}
#e={'S':True}
#print(main(100000, xml_file, X, e))
test_ins()

#var_test = {'bowel-problem': [], 'family-out': [], 'light-on': ['family-out'], 'dog-out': ['bowel-problem', 'family-out'], 'hear-bark': ['dog-out']}
#print(get_right_order(var_test))
