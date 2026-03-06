#Requires AutoHotkey v2.0

F13::
{
    ; Show InputBox to get user command
    result := InputBox(, "Wizard Key", "What should I do?")
    
    ; If cancelled or empty, do nothing
    if result.SpecialKey = "Cancel" or result.Value = ""
        return
    
    userText := result.Value
    projectPath := A_ScriptDir  ; Project root directory
    pythonScript := projectPath . "\wizard\main.py"
    
    ; Create temp file for JSON output
    tempFile := A_Temp . "\wizard_output.json"
    
    ; Build command
    command := 'py "' pythonScript '" "' userText '"'
    
    ; Run Python and capture output to temp file
    RunWait(command " > """ tempFile """",, "Hide")
    
    ; Read JSON response
    jsonOutput := FileRead(tempFile)
    
    ; Parse JSON: extract "ok" boolean
    ok := InStr(jsonOutput, '"ok": true') > 0
    
    ; Parse JSON: extract "message" string
    msgStart := InStr(jsonOutput, '"message": "')
    message := ""
    if msgStart > 0
    {
        msgStart += StrLen('"message": "')
        msgEnd := InStr(jsonOutput, '"', msgStart)
        if msgEnd > msgStart
            message := SubStr(jsonOutput, msgStart, msgEnd - msgStart)
    }
    
    ; Show result to user
    if ok
        MsgBox(message, "Wizard Key - Success")
    else
        MsgBox(message, "Wizard Key - Failed", "Icon!")
    
    ; Clean up temp file
    try
        FileDelete(tempFile)
}
