from winrm.protocol import Protocol
import subprocess
from subprocess import Popen, PIPE, STDOUT
import time

output = ""

t_end = time.time() + 30 
while time.time() < t_end:
    p = Protocol(
        endpoint='http://192.168.0.12:5985/wsman',
        transport='ntlm',
        username='popper\popperuser',
        password='0bserver',
        server_cert_validation='ignore')
    shell_id = p.open_shell()
    command_id = p.run_command(shell_id, 'wmic', ["cpu get loadpercentage"])
    std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
    output+=str(std_out)
    #print(output)
    f = open('/home/dennett/scripting/Scrapings_Popper.txt', 'w')
    f.write(str(output))
    p.cleanup_command(shell_id, command_id)
    p.close_shell(shell_id)
