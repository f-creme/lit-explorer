Set WshShell = CreateObject("WScript.Shell")
AppDir = WScript.ScriptFullName
AppDir = Left(AppDir, InStrRev(AppDir, "\"))  ' Obtenir le répertoire du script VBS

'MsgBox "AppDir: " & AppDir

VenvDir = AppDir & "env\Scripts\activate.bat"
'MsgBox "VenvDir: " & VenvDir

StreamlitCommand = "cmd /c cd /d " & AppDir & " && " & VenvDir & " && streamlit run app.py"
'MsgBox "StreamlitCommand: " & StreamlitCommand

' Lancer Streamlit avec affichage du terminal pour debug
WshShell.Run StreamlitCommand, 1, True
