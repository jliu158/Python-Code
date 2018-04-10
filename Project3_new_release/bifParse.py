import os
import re

#generates a tuple of the assignments by reading the in line comments
def get_assign(line):
    string = re.sub("([\d]+(\.[\d]+)?,[\s]*)+[\d]+(\.[\d]+)?;", "", line).strip()
    if re.match("\(([\w]+,[\s]*)*[\w]+\)", string) is None:
        return tuple([])
    string = re.sub("[\s]+", "", string.lstrip("(").rstrip(")"))
    string = string.upper()
    return tuple(string.split(","))

#replaces comments
def replace_comments(line):
    return re.sub("\(([\w]+,[\s]*)*[\w]+\)", "", line)

#parses bif file
def parse(filename):
    if not os.path.exists(filename):
        return ({}, {}, {})

    vars_dict = {}
    prob_dict = {}
    vars_parent = {}
    name_list = []

    file = open(filename, "r")
    #print "Name of file: " + filename

    line = file.readline()
    
    #variable loop
    while "probability" not in line:

        if line.startswith("variable"):
            name = re.sub("variable[\s]*", "", line.strip())
            name = re.sub("[\s]*\{", "", name)
            name_list.append(name)
            line = file.readline()
            while "discrete" not in line:
                line = file.readline()
            #for diabetes only
            if "//" in line:
                val_temp = []
                vals = re.sub("type[\s]*discrete[\s]*\[[\s]*[\d]+[\s]*\]", "", line.strip())
                vals = re.split('[\{\,\s]+', vals)[1]
                val_temp.append(vals)
                line = file.readline()
                while "};" not in line:
                    vals = re.split('[\{\,\s]+', line)[1]
                    vals = re.split('//', vals)[0]            
                    val_temp.append(vals)
                    line = file.readline()
                vars_dict[name] = val_temp   
            #general condition
            else:
                vals = re.sub("type[\s]*discrete[\s]*\[[\s]*[\d]+[\s]*\]", "", line.strip())
                vals = re.sub("[\{\};\s]+", "", vals)
                vals = vals.split(",")
                vars_dict[name] = vals
        line =file.readline()

    #print vars_dict
    #definitions loop
    while line != "":
        if line.startswith("probability"):
            #index generation
            var_temp = re.sub("probability[\s]*|\{", "", line.strip())
            var_temp = re.sub("[\(\)]+", "", var_temp).strip()
            var_temp = re.sub("[\s\|,]+", ",", var_temp).split(",")
            
            vars_parent[var_temp[0]] = var_temp[1:]       
            var_temp = [var_temp[0], var_temp[1:]]
            prob_dict[var_temp[0]] = {}
            line = file.readline()
            #get each line of table
            while "}" not in line:
                assignment = get_assign(line);
                vals = replace_comments(line).strip()
                vals = re.sub("table", "", vals).strip()
                vals = vals.strip(";")
                vals = vals.split(",")
                for i in range(len(vals)):
                    vals[i] = float(vals[i])
                prob_dict[var_temp[0]][assignment] = vals
                line = file.readline()
        line = file.readline()
    file.close()
    #print prob_dict
    return (vars_dict, prob_dict, vars_parent, name_list)