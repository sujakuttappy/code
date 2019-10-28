
import paramiko
from pathlib import Path
import time
from http import HTTPStatus
import pdb

def handle(req):
    try:
        print("server name:", req)
        HOST = "mgtpp0007"
        PORT = 22
        file = "secret-linux-key"
        #data_folder = Path("/var/openfaas/secrets/")
        #key_file = data_folder / file
        #f = open(key_file)
        #server_key = f.read()

        #Establishing connection to the gatewayserver
        try:
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(hostname = HOST, port = PORT, username="sgarg127", password="Spiderman@112")
            print("successfully connected on port :", HOST)
            try:
                command_pbrun = "pbrun su -"
                pbrun_password= "Spiderman@112"
                command_ssh = "ssh -t"+req
                command_general = "uname -r"
                #command_shutdown = "shutdown -h now"
                wait_time = 5  
                #Invoke shell to execute multiple command_shutdown
                chan = conn.invoke_shell()
                print("PBRun start")
                chan.send(command_pbrun +"\n")
                time.sleep(wait_time)
                chan.send(pbrun_password + "\n")
                time.sleep(wait_time)                      #sleep program for 10 seconds after pbrun server key entered
                resp = chan.recv(9999)
                output = resp.decode('ascii').split(',')
                print (''.join(output))
                if chan.recv_stderr()== False:
                    print(chan.recv_stderr())

                    print(HTTPStatus.INTERNAL_SERVER_ERROR.value)
                # else:
                print("SSH to the server")
                chan.send(command_ssh)
                time.sleep(wait_time)
                if chan.recv_exit_status != 0:
                    print(HTTPStatus.INTERNAL_SERVER_ERROR.value)
                else:
                    print("Execute commands on server")
                    chan.send(command_general + "\n")      # Please  change command to command_shutdown during final execution
                    resp = chan.recv(9999)
                    output = resp.decode('ascii').split(',')
                    print (''.join(output))
                    #print("Waiting for 5 minutes ")  #Uncomment lines 56 - 65 during final execution
                    #time.sleep(300)
                    #print("Checking server connection to see if shutdown is successful or not")
                    #chan.send(command_ssh+"\n")
                    #time.sleep(wait_time)
                    #if chan.channel.recv_exit_status() == 0:
                    #    print("Server is still on. Try again")
                    #else:
                    #    print("Shutdown successful")
                    #conn.close()

            except Exception as e:
                print(HTTPStatus.INTERNAL_SERVER_ERROR.value)
        except Exception as err:
            print(HTTPStatus.BAD_REQUEST.value)           
    except Exception as error:
        print (HTTPStatus.UNAUTHORIZED.value)


handle("apsrd1202")




