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

output = str_uptime + str_free + str_df

f = open('/home/dennett/scripting/Scrapings_Dennett.txt', 'w')
f.write(output)
