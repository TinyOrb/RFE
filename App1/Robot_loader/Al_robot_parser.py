import os
import re

def get_all_robot_ext(path):
    all_file = os.listdir("/home/jaarvis/robot_sample_suite/project1")
    fl = {}
    for f in all_file:
        if re.compile("[a-zA-Z_]+[a-z0-9A-Z_]*.robot$", re.IGNORECASE).match(f):
            fl[os.path.join(path, f)] = f

    return fl

def get_testcases_list(feature, path):
    robot_fl = get_sub_suite(path)
    sl_tc = {}
    sl_tc["feature"] = feature
    sl_tc["suites"] = []
    for pl in robot_fl.keys():
        
        tcs = []
        
        suite = {}

        suite["name"] = robot_fl[pl]
        
        fr = open(pl, "r")
        content = fr.read()
        fr.close()
        
        split_content = content.split("\n")
        
        for li in range(len(split_content)):
            if re.compile("[*]{3}[/\s]{0,1}Test Case[s]{0,1}[/\s]{0,1}[*]{3}[/\s]*", re.IGNORECASE).match(split_content[li]):
                suite_begin = li + 1
                suite_end = None

                for lii in range(li+1, len(split_content)):
                    if re.compile("[/\s]{0,1}[*]+", re.IGNORECASE).match(split_content[lii]):
                        suite_end = lii
                        break
                
                if suite_end == None:
                    suite_end = len(split_content)
                
                print pl, suite_begin, suite_end
                
                for xi in range(suite_begin, suite_end):
                    if re.compile("[/\s]{0,1}[a-zA-Z0-1.:_$#-]+[a-zA-Z/\s0-1.:_$#-]*").match(split_content[xi]):
                        tcs.append(split_content[xi])
        
        suite["tcs"] = tcs
        sl_tc["suites"].append(suite)
    print sl_tc
    
    return sl_tc

def get_sub_suite(path):
    robot_fl = get_all_robot_ext(path)
    sl = {}
    for pl in robot_fl.keys():
        fr = open(pl, "r")
        content = fr.read()
        for cont in content.split("\n"):
            if re.compile("[*]{3}[/\s]{0,1}Test[/\s]{1}Case[s]{0,1}[/\s]{0,1}[*]{3}[/\s]*", re.IGNORECASE).match(cont):
                sl[pl] = robot_fl[pl]
    return sl
