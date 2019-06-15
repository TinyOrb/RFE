Test_Suite_Folder = {
    #"Highball":"C:\\RATF1\\Highball\\testcase",
    #"Boss":"C:\\RATF1\\automation-boss\\TestCases",
    #"CDR-BI":"C:\RATF1\CDR-BI\\Testcase"
    'project1':'/home/shad/workspace_saisei/sample_robot',
    'project2': '/home/shad/workspace_saisei/qa/robot/tests'
    }

def list_robot_files(path):
    try:
        files = [f for f in os.listdir(path) if os.path.isfile(f)]
        wkd = os.path.dirname(os.path.realpath(__file__))
        robot_file = re.compile("^[a-zA-Z0-9_]+.robot$")
        l = []
        count = 1
        for f in files:
            if robot_file.match(f) is not None:
                count = count + 1
                l.append(f)
        return l
    except Exception as e:
        return "Error! " + str(e)

def fetch_All_suite():
    try:
        l = len(Test_Suite_Folder)
        return Test_Suite_Folder
    except Exception as e:
        return "Error! " + str(e)

def fetch_suite_test_cases(suite):
    try:
        path = Test_Suite_Folder[suite]
    except Exception as e:
        return "Error! " + str(e)

def fetch_suite_content(path):
    try:
        pass
    except Exception as e:
        return "Error! " + str(e)

def update_test_suite(path, content):
    try:
        pass
    except Exception as e:
        return "Error! " + str(e)

def execute_scenarios(path, cases):
    try:
        pass
    except Exception as e:
        return "Error! " + str(e)
