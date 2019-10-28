import paramiko
from pathlib import Path
import time
from http import HTTPStatus



def server_shutdown(servername=None):
    try:
        HOST = "40.121.154.135"
        PORT = 22
        file = "secret-server-key"
        data_folder = Path("/var/openfaas/secrets/")
        key_file = data_folder / file
        f = open(key_file)
        server_key = f.read()

        # Establishing connection to the gatewayserver
        try:
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(hostname=HOST, port=PORT, username="kuttappys", password="Abcd!2345678")
            print("successfully connected on port :", HOST)
            try:
                command_pbrun = "pbrun su -"
                command_ssh = "ssh -t" + servername
                command_shutdown = "shutdown -i0 -g60 -y"
                command_general = "uname -r"
                # stdin, stdout, stderr = conn.exec_command(command_pbrun)
                # stdin.write(server_key)
                wait_time = 5
                # Invoke shell to execute multiple command_shutdown
                chan = conn.invoke_shell()
                chan.send(command_ssh)
                time.sleep(wait_time)
                if chan.recv_exit_status != 0:
                    print(HTTPStatus.INTERNAL_SERVER_ERROR.value)
                else:
                    print("Execute commands on server")
                    chan.send(command_general + "\n")  # Please  change command to command_shutdown during final execution
                    resp = chan.recv(9999)
                    output = resp.decode('ascii').split(',')
                    print(''.join(output))
                    # print("Waiting for 5 minutes ")  #Uncomment lines 44 - 53 during final execution
                    # time.sleep(300)
                    # print("Checking server connection to see if shutdown is successful or not")
                    # chan.send(command_ssh+"\n")
                    # time.sleep(wait_time)
                    # if chan.channel.recv_exit_status() == 0:
                    #    print("Server is still on. Try again")
                    # else:
                    #    print("Shutdown successful")
                    # conn.close()

            except Exception as e:
                print(HTTPStatus.INTERNAL_SERVER_ERROR.value)
        except Exception as err:
            print(HTTPStatus.BAD_REQUEST.value)
    except Exception as e:
        print (HTTPStatus.UNAUTHORIZED.value)


server_shutdown()




