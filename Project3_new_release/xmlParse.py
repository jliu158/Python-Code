import os
import re

#replaces all the comments if any present
def replace_comments(line):
    return re.sub("<!--[\w\s!]+-->", "", line)

#trims the tags
def trim(line, delim):
    line = line.strip()
    line = replace_comments(line)
    left = "<" + delim + ">"
    right = "</" + delim + ">"
    line = line.replace(left, "").replace(right, "")
    return line

#generates tuple of the assignments of the current var_temp being added
def get_assign(var_temp, size, vars_dict):
    
    assignment = []
    length = len(var_temp[1])
    for i in range(length):
        pow = 2**(length-i-1)
        num_values = len(vars_dict[var_temp[1][i]])
        assignment.append(vars_dict[var_temp[1][i]][size/pow % (num_values)])
    return tuple(assignment)

#adds a input to the definitions dictionary
def add_defs(line, query, var_temp, vars_dict, temp, prob_dict, index):
    num_values = len(vars_dict[query])
    if line != "":
        table = line.split()
        length = len(table)
        i = 0
        while i < length:
            new_table = []
            for j in range(num_values):
                new_table.append(float(table[i + j]))
            size = len(temp[var_temp])
            assignment = get_assign(var_temp, size, vars_dict)
            temp[var_temp][assignment] = new_table
            prob_dict[index][assignment] = new_table
            i += num_values

#parses input from an xml file
def parse(filename):
    if not os.path.exists(filename):
        return ({}, {}, {})

    vars_dict = {}
    prob_dict = {}
    vars_parent = {}
    name_list = []
    temp = {}
    


    file = open(filename, "r")
    #print "Name of file: " + filename
    line = file.readline()
	
    #variable loop
    while "<DEFINITION>" not in line:

        line = file.readline()
        if "<VARIABLE" in line:
            line = file.readline()
            if "<NAME>" in line:
                name = trim(line, "NAME")
                vars_dict[name] = []
                name_list.append(name)
                line = file.readline()
                while "<OUTCOME>" in line:
                    outcome = trim(line, "OUTCOME")
                    vars_dict[name].append(outcome.upper())
                    line = file.readline()

    while "</BIF>" not in line:
        if "<DEFINITION>" in line:
            line = file.readline()
            if "<FOR>" in line:
                query = trim(line, "FOR")
                var_temp = [query, []]
                
                line = file.readline()
                
                while "<GIVEN>" in line:
                    given = trim(line, "GIVEN")
                    var_temp[1].append(given)
                    line = file.readline()
                    
                vars_parent[var_temp[0]] = var_temp[1]
                index = var_temp[0]          
                prob_dict[index] = {}       
                var_temp[1] = tuple(var_temp[1])
                var_temp = tuple(var_temp)
                temp[var_temp] = {}
                
                while "<TABLE>" in line:
                    line = line.replace("<TABLE>", "")
                    #line = file.readline()
                    while "</TABLE>" not in line:
                        line = replace_comments(line).strip()
                        add_defs(line, query, var_temp, vars_dict, temp, prob_dict, index)
                        line = file.readline()
                    line = replace_comments(line).strip().replace("</TABLE>", "")
                    add_defs(line, query, var_temp, vars_dict, temp, prob_dict, index)
                    line = file.readline()
        line = file.readline()
        #print prob_dict
    file.close()
    
    return (vars_dict, prob_dict, vars_parent, name_list)

a, b, c, d  = parse("aima-alarm.xml")