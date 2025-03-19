@echo off
chcp 65001

set "DOWNLOADS=%USERPROFILE%\Downloads"
set "CHROME_ZIP=%DOWNLOADS%\chrome-win64.zip"
set "CHROMEDRIVER_ZIP=%DOWNLOADS%\chromedriver-win64.zip"
set "CHROME_DIR=Chrome\chrome-win64"
set "CHROMEDRIVER_DIR=Chrome\chromedriver-win64"

REM Criar a pasta Chrome se não existir
IF NOT EXIST "Chrome" mkdir Chrome

REM Baixar e extrair Chrome se não existir
IF NOT EXIST "%CHROME_DIR%" (
    echo Baixando Chrome...
    curl -o "%CHROME_ZIP%" "https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.88/win64/chrome-win64.zip"
    
    REM Extrair no Windows nativo
    powershell -Command "Expand-Archive -Path '%CHROME_ZIP%' -DestinationPath 'Chrome' -Force"
)

REM Baixar e extrair ChromeDriver se não existir
IF NOT EXIST "%CHROMEDRIVER_DIR%" (
    echo Baixando ChromeDriver...
    curl -o "%CHROMEDRIVER_ZIP%" "https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.88/win64/chromedriver-win64.zip"
    
    REM Extrair no Windows nativo
    powershell -Command "Expand-Archive -Path '%CHROMEDRIVER_ZIP%' -DestinationPath 'Chrome' -Force"
)

REM Executar Python
.\python312\python.exe ".\main.py"
