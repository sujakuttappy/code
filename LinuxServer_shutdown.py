import paramiko
from pathlib import Path
import time
from http import HTTPStatus

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
                command_ssh = "ssh -t"+servername+ "shutdown -h now"
                stdin, stdout, stderr = conn.exec_command(command_pbrun)
                #stdin.write(server_key)
                time.sleep(10)                      #sleep program for 10 seconds after pbrun server key entered 
                if stderr.recv_exit_status != 0:
                    raise(HTTPStatus.INTERNAL_SERVER_ERROR.value)
                else:

                    stdin, stdout, stderr = conn.exec_command(command_ssh)
                    if stderr.recv_exit_status != 0:
                        raise(HTTPStatus.INTERNAL_SERVER_ERROR.value)
                    else:

                        print("Waiting for 5minutes to shutdown completely and then try connection is alive or not")
                        time.sleep(300)
                        print("Checking for server connection again to test if shutdown is successful")
                        command = "ssh -t"+servername
                        stdin, stdout, stderr = conn.exec_command(command)
                        if stdout.channel.recv_exit_status() == 0:
                            print("Server is still on. Try again")
                        else:
                            print("Shutdown successful")
            except Exception:
                #print(e)
                raise Exception(HTTPStatus.BAD_REQUEST.value)
        except Exception:
            #print(err)
            raise Exception(HTTPStatus.BAD_REQUEST.value)
            
    except Exception:
        #print(error)
        raise Exception(HTTPStatus.INTERNAL_SERVER_ERROR.value)


server_shutdown()




