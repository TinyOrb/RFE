import xml.etree.ElementTree as ET

def parse_for_test(_file):
    tree = ET.parse(_file)

    root = tree.getroot()
    suite = root.find("suite")
    case_status = {}
    for tests in suite:
        if tests.tag == "test":
            name = tests.attrib["name"]
            for test in tests:
                if test.tag == "status":
                    case_status[name] = test.attrib["status"].lower()+"ed"
    return case_status
