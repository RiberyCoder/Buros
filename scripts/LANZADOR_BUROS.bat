@ECHO OFF
tasklist /FI "USERNAME eq robotltd6" /FI "IMAGENAME eq rocketbot.exe" | find "rocketbot.exe" > NUL
IF "%ERRORLEVEL%" neq "0" (
cd d:
d:
cd D:\Rocketbots_AD\Rocketbot_BUROS_05
rocketbot.exe -db=D:/AD/BUROS_05/robot/buros.db -start=SuperBuros --update_drivers
)