*** Settings ***
Documentation    This is web testing sample suite

Library          Selenium2Library

Suite Setup      Open Google Website
Suite Teardown   Close All Browsers

*** Test Cases ***
Search tinyorb website
    Log  Done

*** Keywords ***
Open Google Website
    ${chrome_options} =     Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    #Call Method    ${chrome_options}   add_argument    headless
    Call Method    ${chrome_options}   add_argument    disable-gpu
    Call Method    ${chrome_options}   add_argument    --no-sandbox
    Call Method    ${chrome_options}   add_argument    --start-maximized
    ${options}=     Call Method     ${chrome_options}    to_capabilities
    Log To Console    ==> Starting the browser headless
    Open Browser    http://www.google.com    browser=chrome    desired_capabilities=${options}
    #Maximize Browser