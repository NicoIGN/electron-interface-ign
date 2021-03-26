@echo OFF

set SCRIPTPATH=%CD%

cd ..
cd ..
set ROOT=%CD%
echo ROOT=%ROOT%
cd %SCRIPTPATH%

REM defining requirements
set SOME_REQUIRED_ENVIRONMENT_VARIABLE=%SCRIPTPATH%
set SOME_REQUIRED_ENVIRONMENT_VARIABLE2=%SCRIPTPATH%


REM launching electron
cd %SCRIPTPATH%

if not exist %SCRIPTPATH%\ihm_minimal.json (
    echo current directory must be where the ihm/json file is located
    exit 1
)

electron -r esm %ROOT%\index.js --ihm %SCRIPTPATH%\ihm_minimal.json
