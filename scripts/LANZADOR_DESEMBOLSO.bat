@ECHO OFF
tasklist /FI "USERNAME eq robotltd3" /FI "IMAGENAME eq rocketbot.exe" | find "rocketbot.exe" > NUL
IF "%ERRORLEVEL%" neq "0" (
cd d:
d:
cd D:\RocketbotAD\Rocketbot_DESEMBOLSO
rocketbot.exe -db=D:/AD/DESEMBOLSO/robot/desembolsos.db -start=00deb00 --update_drivers
)