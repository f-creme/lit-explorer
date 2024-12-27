' ===================================================================================
' app_launcher.vbs
'
' This script is designed to launch the Streamlit application in the virtual environment.
' It automatically identifies the script's directory, activates the virtual environment,
' and runs the Streamlit app (`app.py`).
'
' Author: Florentin Creme
' Date: 12 Dec. 2024
' ===================================================================================

Set WshShell = CreateObject("WScript.Shell")

' Get the directory of the VBS script
AppDir = WScript.ScriptFullName
AppDir = Left(AppDir, InStrRev(AppDir, "\"))

' Path to the virtual environment activation script
VenvDir = """" & AppDir & "env\Scripts\activate.bat" & """"

' Command to activate the virtual environment and launch Streamlit
StreamlitCommand = "cmd /c cd /d """ & AppDir & """ && " & VenvDir & " && streamlit run app.py"

' Uncomment the following line for debugging the constructed command
' MsgBox "StreamlitCommand: " & StreamlitCommand

' Run the Streamlit command in a visible terminal window
' (change the second argument to 0 for a hidden terminal, 1 for a visible terminal, or 2 for a minimized terminal)
WshShell.Run StreamlitCommand, 2, True
