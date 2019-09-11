"""
Copyright 2019, TinyOrb.org

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

@author: Shad Hasan, Tinyorb.Org
"""
import os
import re
import json

def get_all_robot_ext(path):
    all_file = os.listdir(path)
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
            if re.compile("[*]{3}[/\s]{0,1}Test[/\s]{0,1}Case[s]{0,1}[/\s]{0,1}[*]{3}[/\s]*", re.IGNORECASE).match(split_content[li]):
                suite_begin = li + 1
                suite_end = None

                for lii in range(li+1, len(split_content)):
                    if re.compile("[/\s]{0,1}[*]+", re.IGNORECASE).match(split_content[lii]):
                        suite_end = lii
                        break
                
                if suite_end == None:
                    suite_end = len(split_content)
                
    #            print pl, suite_begin, suite_end
                
                for xi in range(suite_begin, suite_end):
                    if re.compile("[/\s]{0,1}[a-zA-Z0-1.:_$-]+[a-zA-Z/\s0-1.:_$#-]*").match(split_content[xi]):
                        tcs.append({"name":split_content[xi]})
        
        suite["tcs"] = tcs
        sl_tc["suites"].append(suite)
    # print sl_tc
    
    return sl_tc


def get_tag_list(path, suite):

    fr = open(os.path.join(path, suite), "r")
    content = fr.read()
    fr.close()
    tags = []
    split_content = content.split("\n")
    try:
        for li in range(len(split_content)):
            if re.compile("[*]{3}[/\s]{0,1}Test[/\s]{0,1}Case[s]{0,1}[/\s]{0,1}[*]{3}[/\s]*", re.IGNORECASE).match(
                    split_content[li]):
                suite_begin = li + 1
                suite_end = None

                for lii in range(li + 1, len(split_content)):
                    if re.compile("[/\s]{0,1}[*]+", re.IGNORECASE).match(split_content[lii]):
                        suite_end = lii
                        break

                if suite_end == None:
                    suite_end = len(split_content)

                #print(suite_begin, suite_end)

                for xi in range(suite_begin, suite_end):
                    if re.compile("[/\s]{2,4}\[TAGS][/\s]{2,4}[/\sa-zA-Z0-9_-]+", re.IGNORECASE).match(split_content[xi]):
                        possible_tag = split_content[xi].replace("[TAGS]", "").split("  ")
                        for tag in possible_tag:
                            if tag.strip() != "":
                                tags.append(tag.strip())
    except Exception as e:
        print("Exception as %s" % str(e))
    return tags


def get_sub_suite(path):
    robot_fl = get_all_robot_ext(path)
    sl = {}
    for pl in robot_fl.keys():
        fr = open(pl, "r")
        content = fr.read()
        for cont in content.split("\n"):
            if re.compile("[*]{3}[/\s]{0,1}Test[/\s]{0,1}Case[s]{0,1}[/\s]{0,1}[*]{3}[/\s]*", re.IGNORECASE).match(cont):
                sl[pl] = robot_fl[pl]
    return sl


def read_robot_content(path):
    try:
        fr = open(os.path.join(path), "r")
        content = fr.read()
        fr.close()
        mtime = os.stat(path).st_mtime
        return {"data": content, "mtime": mtime*1000}
    except Exception as e:
        print("Error as %s" % str(e))
        return None


def write_robot_content(path, content):
    try:
        f = open(path, "w")
        f.write(content)
        f.close()
        return True
    except Exception as e:
        print("Error as %s" % str(e))
        return None


def delete_content(path, ftype):
    try:
        if os.path.isdir(path) and ftype == "folder":
            os.rmdir(path)
            status = True
        elif os.path.isfile(path) and ftype == "file":
            os.remove(path)
            status = True
        else:
            status = False
    except Exception as e:
        print("Error as %s" % str(e))
        status = False
    return status


def add_content(path, ftype):
    try:
        if ftype == "file":
            with open(path, "w+") as f:
                f.close()
            status = True
        elif ftype == "folder":
            os.mkdir(path)
            status = True
        else:
            status = False
    except Exception as e:
        print("Error as %s" % str(e))
        status = False
    return status


def deploy_feat(template, feat_name, workspace):
    try:
        print("deploying project from template: %s"%template)
        with open("App1/project_template.json") as json_file:
            data = json.load(json_file)
        structure = data["templates"][template]
        folder_path = {}
        file_path = {}
        code_data = {}
        folder_path[0] = os.path.join(workspace, feat_name)
        for folder_key in structure["folder"].keys().sort():
            parent = int(re.findall("\$d([0-9]+)/", structure["folder"][folder_key])[0])
            sub = structure["folder"][folder_key].split("/")[1]
            folder_path[folder_key] = os.path.join(folder_path[parent], sub)
        for file_key in structure["file"].keys().sort():
            parent = int(re.findall("\$d([0-9]+)/", structure["file"][file_key])[0])
            sub = structure["file"][file_key].split("/")[1]
            file_path[file_key] = os.path.join(folder_path[parent], sub)
        for data_key in structure["sampleCode"].keys().sort():
            findex = int(re.findall("\$f([0-9]+)/", data_key)[0])
            code_data[file_path[findex]] = structure["sampleCode"][data_key]

        for key in folder_path:
            add_content(folder_path[key], "folder")
        for key in file_path:
            add_content(file_path[key], "filer")
        for key in code_data:
            write_robot_content(key, code_data[key])

        status = True
        print("Template deployed successfully")
    except Exception as e:
        print("Error as %s" % str(e))
        status = False
    return status
