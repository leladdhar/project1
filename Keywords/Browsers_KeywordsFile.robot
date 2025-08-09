*** Keywords ***
Check And Get Version
    [Arguments]    ${exe_path}    ${browser_name}
    ${exists}=    Run Keyword And Return Status    File Should Exist    ${exe_path}
    Run Keyword If    ${exists}    Get Version From Path    ${exe_path}    ${browser_name}
    ...    ELSE    Log    ❌ ${browser_name} is not installed at expected path: ${exe_path}

Get Version From Path
    [Arguments]    ${exe_path}    ${browser_name}
    ${command}=    Set Variable    (Get-Item "${exe_path}").VersionInfo.ProductVersion
    ${result}=     Run Process    powershell    -Command    ${command}    shell=True    stdout=PIPE    stderr=PIPE
    ${version}=    Set Variable    ${result.stdout.strip()}
    Log    ✅ ${browser_name} Version: ${version}
    Log To Console    ✅ ${browser_name} Version: ${version}