*** Settings ***
Documentation    This is web testing sample suite

Library          Selenium2Library

Suite Setup      Open Google Website
Suite Teardown   Close All Browsers

*** Variables ***
${count}   ${1}

*** Test Cases ***
Search tinyorb website
    Wait Until Element Is Visible   xpath=//input[@name='q']   60S
    sleep   10S
    Click Element   xpath=//input[@name='q']
    Input Text   xpath=//input[@name='q']    tinyorb.org
    Press Key    xpath=//input[@name='q']    \\13
    Wait Until Element Is Visible   xpath=//div[@class='r']   60S
    Sleep   10S
    ${results}=    Get WebElements    xpath=//div[@class='r']
    :FOR    ${result}    IN    @{results}
    \   ${text}=    Get Text    ${result}
    \   Log To Console    Search Result ${count}: ${text}
    \   ${count}=  Evaluate  ${count}+1


*** Keywords ***
Open Google Website
    ${chrome_options} =     Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${chrome_options}   add_argument    headless
    Call Method    ${chrome_options}   add_argument    disable-gpu
    Call Method    ${chrome_options}   add_argument    --no-sandbox
    Call Method    ${chrome_options}   add_argument    --start-maximized
    ${options}=     Call Method     ${chrome_options}    to_capabilities
    Log To Console    ==> Starting the browser headless
    Open Browser    http://www.google.com    browser=chrome    desired_capabilities=${options}
    #Maximize Browser