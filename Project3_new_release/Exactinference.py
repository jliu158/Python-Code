#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 19:19:15 2017

@author: zhao
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import xml.dom.minidom
import matplotlib.pyplot as plt
import time
import xmlParse as xp
import bifParse as bp
import copy

def P_child_parent(child, evidences):
    # child of definition
    #if child.values()==[True]:
    #    return 0.4
    #else:
    #    return 0.5
    
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
            #print(parent_str)
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



def ENUMERATION_ASK(X,e,bn,VARS):
  
    Q_X=[0]*len(Name(X))
    Q_X_norm=[0]*len(Name(X))
    e_xi = e
    
    i=0
    for name in Name(X):
        e_xi[X]=name
        Q_X[i]=ENUMERATE_ALL(VARS,e_xi)
        i+=1
         
    norm=sum(Q_X)
    for j in xrange(len(Name(X))):
        Q_X_norm[j]=Q_X[j]/norm
    
    output={}
    for value in Q_X_norm:
         output[Name(X)[Q_X_norm.index(value)]]=value
    return output
    #return Q_X_norm

def ENUMERATE_ALL(vars,e): 
    if vars==[]:
        return 1
        
    else:
        Y=vars[0]

    vars_new=[]
    for item in vars:
        if item!=vars[0]:
            vars_new.append(item)
    
    if Y in e:
        y=e[Y]
        #print(Name)
        #index=Name(Y).index(y)
        P=get_value_out(Y, y ,e)
        return P*ENUMERATE_ALL(vars_new,e)
    
    else:
        Sum=0
        for name in Name(Y):
            Y_dict={Y:name}
            e_y=dict(e, **Y_dict)
            P=get_value_out(Y, name ,e)
            Sum=Sum+P*ENUMERATE_ALL(vars_new,e_y)
        
        return Sum

def main_bey(xml_file, X, e):
    '''
    global definition
    #tic = time.time()
    
    dom = xml.dom.minidom.parse(xml_file)
    root = dom.documentElement
    definition = root.getElementsByTagName('DEFINITION')
    
    VARS = []
    variables = root.getElementsByTagName('VARIABLE')
    for variable in variables:
        VARS.append(variable.getElementsByTagName('NAME')[0].firstChild.data)
    '''
    bn=0
    global name_list
    VARS = name_list
    ENUMERATION_ASK(X,e,bn,VARS)
    #toc = time.time()
    #print('That took %fs' % (toc - tic))
    return (ENUMERATION_ASK(X,e,bn,VARS))

def Prob(X,e):
    
   # List=[]
   # for name in Name(X):
   #     List.append(float(P_child_parent({X:name}, e)))
   # return List
    return get_value_list(X,e)
        
def Name(X):
    #return [True,False]
    return get_var_domain(X)
def test_ins():
    
    global var_domain, prob_dict, var_parent, name_list
    
    while True:
        
        xml_file, X, e= input('Please type in the instructions to test: ')
        
        file_name=xml_file
        if file_name[-3:]=='bif':
            var_domain, prob_dict, var_parent, name_list = bp.parse(file_name)
            var_parent_copy = copy.deepcopy(var_parent)
            name_list = get_right_order(var_parent_copy)
        elif file_name[-3:]=='xml':
            var_domain, prob_dict, var_parent, name_list = xp.parse(file_name) # xml parser py
            var_parent_copy = copy.deepcopy(var_parent)
            name_list = get_right_order(var_parent_copy)
        tic = time.time()
        result = main_bey(xml_file, X, e)
        toc = time.time()
        print('The result is {0} and time spent is {1} seconds').format(result, toc-tic)


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
    
#xml_file = 'aima-alarm.xml'
#X='B'
#e={'J':'true','M':'true'}
#xml_file = 'aima-wet-grass.xml'
#X='R'
#e={'S':'true'}
#main_bey(xml_file, X, e)

test_ins()


