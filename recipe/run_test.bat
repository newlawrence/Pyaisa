CD %SRC_DIR%
py.test pyaisa
IF %ERRORLEVEL% NEQ 0 EXIT /B %ERRORLEVEL%
