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
    script_key_list = []
    style_key_list = []
    # rawheaderscript, rawbodyprescript, rawbodypostscript
    script_key_list = get_script_key_list(param)
    script_key_list.sort()
    st = ""
    for key in script_key_list:
        print key
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
        st = st + param[key]

    for bkey in body_script_key:
        st = st + "<script type=text/javascript src=" + param[bkey] + " ></script>"
    return st
