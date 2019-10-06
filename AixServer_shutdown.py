def server_shutdown(servername= None):
    try:
        import paramiko
        import os
        import platform
        from pathlib import Path
        import time
        
        HOST = "mgtpp0008"
        PORT = 22
        file = "secret-server-key"
        #data_folder = Path("/var/openfaas/secrets/")
        #key_file = data_folder / file
        #f = open(key_file)
        #server_key = f.read()

        #Establishing connection to the gatewayserver
        try:
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(hostname = HOST, port = PORT, username="skutta1", password="1Optum23")
            print("successfully connected on port :", HOST)
            try:
                command = "ssh -t"+servername+ "sudo shutdown -h now"
                stdin, stdout, stderr = conn.exec_command(command)
                stdin.write(serverkey)
                print("Waiting for 10 seconds to shutdown completely and then try connection is alive or not")
                time.sleep(10)
                command = "ssh -t"+servername
                stdin, stdout, stderr = conn.exec_command(command)
                if #if stdout.channel.recv_exit_status() != 0:

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




