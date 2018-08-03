import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.0.53', username='hyp1', password='0bserver')

stdin, stdout, stderr = ssh.exec_command("uptime")
uptime = stdout.readlines()
#print('uptime: ', uptime, type(uptime))
str_uptime = str(uptime)

stdin, stdout, stderr = ssh.exec_command("free")
free = stdout.readlines()
#print('free: ', free, type(free))
str_free = str(free)

stdin, stdout, stderr = ssh.exec_command("df -h")
df = stdout.readlines()
#print('df -h: ', df, type(df))
str_df = str(df)

output = str_uptime + str_free + str_df

f = open('/home/dennett/scripting/Scrapings_Hyp1.txt', 'w')
f.write(output)

