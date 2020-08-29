FOR /f "tokens=*" %%a in ('dir * /s/b ^| findstr /r ".*\\migrations\\.*.py$" ^| findstr /v "__init__.py$"') do del %%a
FOR /f "tokens=*" %%a in ('dir * /s/b ^| findstr /r ".*\\migrations\\.*.pyc$"') do del %%a
del db.sqlite3
