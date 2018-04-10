# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 01:51:37 2017

@author: Zhao
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import  xml.dom.minidom
import numpy as np
import matplotlib.pyplot as plt
import time
import xmlParse as xp
import copy
import bifParse as bp
#import exact_inference_new as bnb


def main(N, xml_file, X, e):
    global definition
    global name_list
    dom = xml.dom.minidom.parse(xml_file)
    root = dom.documentElement
    definition = root.getElementsByTagName('DEFINITION')
    
    VARS = []
    variables = root.getElementsByTagName('VARIABLE')
    for variable in variables:
        VARS.append(variable.getElementsByTagName('NAME')[0].firstChild.data)
    
    VARS=name_list
    bn='niubi'
    
    return REJECTION_SAMPLING(X,e,bn,N,VARS)



def REJECTION_SAMPLING(X,e,bn,N,VARS):

    count={}
    for name in Name(X):
        count[name]=0
        
    for j in range(N):
        samples=PRIOR_SAMPLE(VARS)
        Consistency=consistency(samples,e)
        
        if Consistency==True:
            count[samples[X]]+=1
            
    Sum=0
    for key in count:
        Sum=Sum+count[key]
            
    for name in count:
        count[name]=float(count[name])/Sum
              
    return count

def consistency(samples,e):

    for item in e:
            if e[item]!=samples[item]:
                return False
            else:
                niubi=1
    return True
    
    
def random(prob,X):

    random=np.random.uniform(0,1)
    i=0
    Sum=0
    for value in prob:
        Sum=Sum+value
        if random<Sum:
            return (Name(X))[i]
        i+=1
    
    
def PRIOR_SAMPLE(VARS):
    
    sample={}
    for j in range(len(VARS)):
        if j<=len(VARS):
            
            prob=Prob(VARS[j],sample)
            sample[VARS[j]]=random(prob,VARS[j])
            
    return sample

         
def Prob(X,e):
    
    return get_value_list(X,e)
        
def Name(X):
  
    return get_var_domain(X)

def test_ins():
    global var_domain, prob_dict, var_parent, name_list
    
    while True:
        N, xml_file, X, e = input('Please type in the instructions to test: ')
        
        file_name=xml_file
        if file_name[-3:]=='bif':
            
            x=bp.parse(file_name)
            
            var_domain, prob_dict, var_parent, name_list = bp.parse(file_name)
            
            var_parent_copy = copy.deepcopy(var_parent)
            name_list = get_right_order(var_parent_copy)
        elif file_name[-3:]=='xml':
            var_domain, prob_dict, var_parent, name_list = xp.parse(file_name) # xml parser py
            var_parent_copy = copy.deepcopy(var_parent)
            name_list = get_right_order(var_parent_copy)
            
        tic = time.time()
        result = main(N, xml_file, X, e)
        toc = time.time()
        print('The result is {0} and time spent is {1} seconds').format(result, toc - tic)


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
            parent_tuple += (str(evidence[p]),)
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
   

number_of_samples=[]
Time=[]
error=[]

#xml_file = 'aima-alarm.xml'
#X='B'
#e={'J':True,'M':True}

#xml_file = 'aima-wet-grass.xml'
#X='R'
#e={'S':True}

#N=10000
#main(xml_file, X, e,N)     

test_ins()


