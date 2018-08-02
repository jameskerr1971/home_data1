#import os

#ssh = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh.connect('192.168.0.11', username='admin', password='alahr0hh')

#stdin, stdout, stderr = os.system("uptime")
#uptime = stdout.readlines()
#print('uptime: ', uptime, type(uptime))
#str_uptime = str(uptime)

import subprocess as sub

p = sub.Popen(['uptime'],stdout=sub.PIPE,stderr=sub.PIPE)
uptime = p.communicate()
print(uptime)
str_uptime = str(uptime)

p = sub.Popen(['free'],stdout=sub.PIPE,stderr=sub.PIPE)
free = p.communicate()
print(free)
str_free = str(free)

p = sub.Popen(['df'],stdout=sub.PIPE,stderr=sub.PIPE)
df = p.communicate()
print(df)
str_df = str(df)


#stdin, stdout, stderr = ssh.exec_command("top -b -n 1")
#top = stdout.readlines()
#print('top: ', top, type(top))
#str_top = str(top)

#stdin, stdout, stderr = os.exec_command("free")
#free = stdout.readlines()
#print('free: ', free, type(free))
#str_free = str(free)

#stdin, stdout, stderr = os.exec_command("df -h")
#df = stdout.readlines()
#print('df -h: ', df, type(df))
#str_df = str(df)

output = str_uptime + str_free + str_df

f = open('/home/dennett/scripting/Scrapings_Dennett.txt', 'w')
f.write(output)
