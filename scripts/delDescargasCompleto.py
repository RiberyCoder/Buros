from os import system
system('rd {rutaPadre}descargas /s /q')
system('del C:\Users\{userPc}\Downloads\*.pdf /s /q')
system('md {rutaPadre}descargas')
system('del {rutaPadre}atenciones\buros.xlsx')