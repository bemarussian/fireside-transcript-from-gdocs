*** Settings ***
Library    SeleniumLibrary

*** Variables ***
# Set browser , # headlesschrome
${BROWSER}    chrome
${URL}        https://app.fireside.fm/login
${username}   your_username
${password}   Your_password
# Used to set selenium speed (i.e. delay) when waiting for browser load
${speed}                 3 seconds
${ep_edit_url}           https://app.fireside.fm/podcasts/transcript-tst/episodes/b0cd4cc6-8f99-4907-89fd-1a001ee75b1f/edit
${ep_transcript_file}    /Users/sergey/Documents/Python-projects/fireside-transcript-from-gdocs/src/dev/transcripts/e0.txt

*** Keywords ***
Get xpath
    [Arguments]   ${element}   ${parameter}=''

    IF        "${element}" == "login_username"
        ${res}=   Set Variable   xpath=//*[@id="email"]
    ELSE IF   "${element}" == "login_pass"
        ${res}=   Set Variable   xpath=//*[@id="password"]
    ELSE IF   "${element}" == "login_button"
        ${res}=   Get WebElement   xpath=//*[@type="submit"]
    ELSE IF   "${element}" == "welcome_content"
        ${res}=   Set Variable   xpath=//*[@data-dismiss="alert"]
    ELSE IF   "${element}" == "transcript_panel"
        ${res}=   Set Variable   xpath=//*[@aria-controls="transcript-panel"]
    ELSE IF   "${element}" == "transcript_upload"
        ${res}=   Set Variable   xpath=//*[@id="transcript_upload_url"]
    ELSE IF   "${element}" == "episode_form_submit_button"
        ${res}=   Set Variable   xpath=//*[@id="episode_form_submit_button"]
    END

    [return]   ${res}

*** Test Cases ***
Login to Fireside.fm
    ${speed}=  Set Selenium Speed   ${speed}
    Open Browser    ${URL}    ${BROWSER}
    ${speed}=  Set Selenium Speed   ${speed}

    ${element}=   Get xpath   login_username
    Input Text   ${element}   ${username}

    ${element}=   Get xpath   login_pass 
    Input Password  ${element}  ${password}

    ## Click on Login
    ${element}=   Get xpath   login_button 
    Click Element     ${element}

    # added waitng for element due to fals login errors in EU Non-PROD
    ${element}=   Get xpath   welcome_content 
    Wait Until Page Contains Element   ${element}

Open Episode edit Page
    ${speed}=  Set Selenium Speed   ${speed}
    Go To  ${ep_edit_url}
    ${speed}=  Set Selenium Speed   ${speed}
    ## Click on Transcript extend
    ${element}=   Get xpath   transcript_panel 
    Click Element     ${element}
    ## Click on Transcript upload
    ${element}=   Get xpath   transcript_upload 
    Choose File     ${element}   ${ep_transcript_file} 
    ## Wait for upload
    Wait Until Page Contains    Upload Complete!

    ## Click on Update
    ${element}=   Get xpath   episode_form_submit_button 
    ${speed}=  Set Selenium Speed   ${speed}
    Click Element     ${element}
    ${speed}=  Set Selenium Speed   ${speed}

    ## Wait for update
    Wait Until Page Contains    Episode was successfully updated.

Clear up - close
    Close Browser
