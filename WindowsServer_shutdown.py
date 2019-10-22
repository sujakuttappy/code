import paramiko
from pathlib import Path
import time
        

def server_shutdown(servername= None):
    try:
        HOST = "13.90.142.73"
        PORT = 22
        file = "secret-server-key"
        # data_folder = Path("/var/openfaas/secrets/")
        # key_file = data_folder / file
        # f = open(key_file)
        # server_key = f.read()

        #Establishing connection to the gatewayserver
        try:
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(hostname = HOST, port = PORT, username="kuttappys", password="Abcd!2345678")
            print("Successfully connected on gateway server :", HOST)
            try:
                command_ssh  = "ssh"+servername 
                stdin, stdout, stderr = conn.exec_command(command_ssh)
                stdin.write(server_key)
                time.sleep(10)               
                stdin, stdout, stderr = conn.exec_command("shutdown /s /f")
                print("Waiting for 3 mins to shutdown completely and then try connection  if it is alive or not")
                time.sleep(180)
                print("Checking for server connection again to test if shutdown is successful")
                command = "ssh"+servername
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




