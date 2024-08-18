Dim WshShell
Set WshShell = CreateObject("Wscript.Shell")
WshShell.Run "cmd /c ""D:\dev\Tarefas\.venv\Scripts\activate & python main.py""", 0, True
Set WshShell = Nothing