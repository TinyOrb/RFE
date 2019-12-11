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
import re

def htmlstructure(**param):
    html = "<html>"
    html = html + "<head>" + headstructure(param) + "</head>"
    html = html + "<body>" + bodystructure(param) + "</body>"
    html = html + "</html>"
    return html

def get_script_key_list(param):
    all_keys = param.keys()
    script_key_list = []
    script = re.compile("script\$*", re.IGNORECASE)
    for key in all_keys:
        ret = script.match(key)
        if ret != None:
            script_key_list.append(key)
    return script_key_list

def get_head_raw_script_key_list(param):
    all_keys = param.keys()
    head_raw_script_key_list = []
    script = re.compile("headrawscript\$*", re.IGNORECASE)
    for key in all_keys:
        ret = script.match(key)
        if ret != None:
            head_raw_script_key_list.append(key)
    return head_raw_script_key_list

def get_head_raw_key_list(param):
    all_keys = param.keys()
    head_raw_key_list = []
    raw = re.compile("headrawmeta\$*", re.IGNORECASE)
    for key in all_keys:
        ret = raw.match(key)
        if ret != None:
            head_raw_key_list.append(key)
    return head_raw_key_list

def get_style_key_list(param):
    all_keys = param.keys()
    style_key_list = []
    style = re.compile("style\$*", re.IGNORECASE)
    for key in all_keys:
        ret = style.match(key)
        if ret != None:
            style_key_list.append(key)
    return style_key_list

def get_body_key_list(param):
    all_keys = param.keys()
    body_key_list = []
    body_script_key_list = []
    body = re.compile("body\$*", re.IGNORECASE)
    for key in all_keys:
        ret = body.match(key)
        if ret != None:
            body_key_list.append(key)

    script = re.compile("bscript\$*", re.IGNORECASE)
    for key in all_keys:
        ret = script.match(key)
        if ret != None:
            body_script_key_list.append(key)

    return body_key_list, body_script_key_list

def headstructure(param):
    # rawheaderscript, rawbodyprescript, rawbodypostscript
    st = ""

    raw_key_list = get_head_raw_key_list(param)
    raw_key_list.sort()
    for key in raw_key_list:
        st = st + param[key]

    script_key_list = get_script_key_list(param)
    script_key_list.sort()
    for key in script_key_list:
        st = st + "<script type=text/javascript src=" + param[key] + " ></script>"

    style_key_list = get_style_key_list(param)
    style_key_list.sort()
    for key in style_key_list:
        st = st + "<link type='text/css' rel='stylesheet' href=" + param[key] + " >"

    head_raw_script_key_list = get_head_raw_script_key_list(param)
    head_raw_script_key_list.sort()
    st = st + "<script>"
    for key in head_raw_script_key_list:
        st = st + param[key]
    st = st + "</script>"
    return st

def bodystructure(param):
    body_key_list = []
    body_key_list, body_script_key = get_body_key_list(param)
    body_key_list.sort()
    st = ""
    for key in body_key_list:
        st = "{}{}".format(st, param[key])

    for bkey in body_script_key:
        st = st + "<script type=text/javascript src=" + param[bkey] + " ></script>"
    return st
