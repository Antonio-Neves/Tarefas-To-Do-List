@echo off

REM Caminho da pasta onde está o virtualenv e o script python
set "virtualenv_path=D:/dev/Tarefas/.venv"
set "script_path=D:/dev/Tarefas/main.py"

REM Navegando até o diretório do virtualenv
cd /d "%virtualenv_path%"

REM Ativando o virtualenv
call Scripts\activate.bat

REM Executando o script Python
python "%script_path%"

REM Desativando o virtualenv
deactivate