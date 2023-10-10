import subprocess
result = subprocess.run(["{rutaPadre}scripts/query.exe", "session"], stdout=subprocess.PIPE)
y = result.stdout
x=y.decode('latin-1')
x=x.split('\n')
for q in x:
  if str("{userPc}") in q:
    break
q=q.split()
z= q[0]
z=z.replace(">","")
nd='TASKLIST /FI "SESSIONNAME eq '+z+'" /FI "IMAGENAME eq EXCEL.EXE"'
result2 = subprocess.run(nd, stdout=subprocess.PIPE)
p = result2.stdout
o=p.decode('latin-1')
print(o)
j=o.split('EXCEL.EXE')[1].strip().split(' ')[0]
print(j)
os.system('TASKKILL /F /PID '+j)