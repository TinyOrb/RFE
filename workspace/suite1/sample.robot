*** Settings ***
Documentation    This is sample robot file

*** Variables ***
${expected_animal}=    Lion

*** Test Cases ***
TC001 Verify animal is lion
    Verifying animal is    animal=Lion

TC002 Verify animal is lion
    Verifying animal is    animal=Tiger

TC1004 Verify nothing
    Log   who cares

*** Keywords ***
Verifying animal is
    [Arguments]    ${animal}
    Should be Equal    ${animal}    ${expected_animal}
