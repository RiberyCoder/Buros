import os
from datetime import datetime

hor = datetime.now().strftime('%d/%m/%Y %H:%M')

file = open("C:/LOGS/ROBOT1.txt", "w")
file.write(hor + os.linesep)
file.close()
