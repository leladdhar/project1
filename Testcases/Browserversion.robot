*** Settings ***
Library           Process
Library           Dialogs
Library           String
Library           OperatingSystem
#Library    RequestsLibrary
Resource    ../../../PycharmProjects/project1/Keywords/Browsers_KeywordsFile.robot
Resource    ../../../PycharmProjects/project1/Variables/Variables.robot

*** Test Cases ***
Get Browser Version Based On User Input
    ${result}=    Run Process    powershell    -Command    Read-Host "Enter browser name (chrome / edge / firefox)"    shell=True    stdout=PIPE
    ${browser}=   Set Variable    ${result.stdout.strip()}
#    ${browser}=    Get Value From User    Enter browser name (chrome / edge / firefox):
    ${browser}=    Convert To Lowercase    ${browser}

    Run Keyword If    '${browser}' == 'chrome'    Check And Get Version    ${CHROME_PATH}    Chrome
    ...    ELSE IF    '${browser}' == 'edge'      Check And Get Version    ${EDGE_PATH}    Edge
    ...    ELSE IF    '${browser}' == 'firefox'      Check And Get Version    ${FIREFOX_PATH}    Firefox
    ...    ELSE    Log    ❌ Invalid browser name entered: ${browser}