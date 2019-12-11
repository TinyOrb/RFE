**************************************************************************
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

@author: Shad Hasan, Tinyorb.org
**************************************************************************


Requirement for manual installation
-----------------------------------
Python 2.7

Djnago 1.11

Robotframework

other python package

Start Application
-----------------
It is django application. So go to installation directory and run django application.

$> python RFE/manage.py runserver

Test application installation
-----------------------------
Browse application by using below url.

http://127.0.0.1:8000/RFE

*************************
Automated installation
*************************
Currently, we have installer for ubuntu, centos and opensuse.

Follow url https://github.com/TinyOrb/RFE/releases and download installer.tar.gz. Then

$> tar -xvf installer.tar.gz

$> cd bundle

$> sudo ./install.sh

Navigate http://127.0.0.1:8000/RFE on your browser.

************************
How To Configure Project
************************
Go to App1/meta.json file and update below json file with desired project name with path in Test_Suite_Folder.

```json
{
"Test_Suite_Folder": {
    "project1":"workspace/suite1"
    },

"Variable_File" :{
    "project1": null
},

"CWD" : {
    "project1": null
},

"ENV_Path": {
    "project1": {}
    }
}
```
-----------
Definition:
-----------
Test_Suite_Folder: You can provide the path of robot framework suite path. This is like basic requirement for project to be added.

Variable_File: This can be used to locate variable file as optional parameter. You may want to provide robot framework.

CWD: This can be used to set current working directory for project.

ENV_Path: This can be used to provide environment variable along value.


Sample:

```json
"project2": {
        "PYTHONPATH": ["/home/shad/sample/qa/robot/lib"],
        "PATH": ["/home/shad/sample/qa/robot/lib/geckodriver"]
    }
```
-------------
Verification:
-------------
Navigate http://127.0.0.1:8000/RFE

Click on Run on WEB_TESTING_SAMPLE.ROBOT

Click on view

If everything goes as planned, wait to script log "Completed".

