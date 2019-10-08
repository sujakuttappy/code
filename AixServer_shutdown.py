import paramiko
from pathlib import Path
import time
        

def server_shutdown(servername= None):
    try:
        HOST = "40.121.154.135"
        PORT = 22
        file = "secret-server-key"
        data_folder = Path("/var/openfaas/secrets/")
        key_file = data_folder / file
        f = open(key_file)
        server_key = f.read()

        #Establishing connection to the gatewayserver
        try:
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(hostname = HOST, port = PORT, username="kuttappys", password="Abcd!2345678")
            print("successfully connected on port :", HOST)
            try:
                command_pbrun = "pbrun su -"
                command_ssh = "ssh -t"+servername+ "shutdown  -force"
                stdin, stdout, stderr = conn.exec_command(command_pbrun)
                stdin.write(server_key)
                time.sleep(10)                      #sleep program for 10 seconds after pbrun server key entered 
                stdin, stdout, stderr = conn.exec_command(command_ssh) 
                print("Waiting for 5minutes to shutdown completely and then try connection is alive or not")
                time.sleep(300)
                print("Checking for server connection again to test if shutdown is successful")
                command = "ssh -t"+servername
                stdin, stdout, stderr = conn.exec_command(command)
                if stdout.channel.recv_exit_status() == 0:
                    print("Server is still on. Try again")
                else:
                    print("Shutdown successful")
            except Exception as e:
                print("Error while executing commands on gateway server", e)
        except Exception as err:
            print("Error in connecting gateway server", err)
    except Exception as e:
        status_message = "Initial connection establishment error"
        print(status_message, e)


server_shutdown()




