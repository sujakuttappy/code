import paramiko
from pathlib import Path
import time
import wmi
from http import HTTPStatus


def server_shutdown(servername=None):
    try:
        HOST = "13.90.142.73"
        PORT = 22
        file = "secret-server-key"
        username = "kuttappys"
        password = "Abcd!2345678"
        # data_folder = Path("/var/openfaas/secrets/")
        # key_file = data_folder / file
        # f = open(key_file)
        # server_key = f.read()

        # Establishing connection to the gatewayserver
        try:
            # Connecting via RDP to gateway
            conn = wmi.WMI(HOST, user=username, password=password)

            # Connection via ssh to gateway
            # conn = paramiko.SSHClient()
            # conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # conn.connect(hostname = HOST, port = PORT, username= username, password = password)
            print("Successfully connected on gateway server :", HOST)
            try:
                command_rdp_server = "mstsc" + servername
                general_command = "ver"
                # shutdown_command = "shutdown /s /f"   #Uncomment this during final execution
                process_id, return_value = conn.Win32_Process.Create(CommandLine=command_rdp_server)
                time.sleep(5)
                process_id, return_value = conn.Win32_Process.Create(CommandLine=server_key)
                if return_value != 0:
                    print(HTTPStatus.BAD_REQUEST.value)
                else:
                    print("Executing general command on server")
                    process_id, return_value = conn.Win32_Process.Create(CommandLine=general_command)
                    time.sleep(2)
                    if return_value != 0:
                        print(HTTPStatus.INTERNAL_SERVER_ERROR.value)
                    else:
                        print("process id:", process_id)
                        # print("executing shutdown command")  #Uncoment till else block  from here during final execution
                        # process_id, return_value = conn.Win32_Process.Create(CommandLine=shutdown_commmand)
                        # print("Waiting for 5 minutes to proces shutdown")
                        # time.sleep(300)
                        # if return_value != 0:
                        #     print(HTTPStatus.INTERNAL_SERVER_ERROR.value)
                        # else:
                        #     print("check if shutdown is successful or not  by running rdp command again")
                        #     process_id, return_value = conn.Win32_Process.Create(CommandLine=command_rdp_server)
                        #     time.sleep(5)
                        #     if return_value == 0:
                        #         print("Server is still on")
                        #     else:
                        #         print("Server shutdown successful")

                # command_ssh = "ssh" + servername
                # chan = conn.invoke_shell()

                # chan.send(command_ssh + "\n")
                # time.sleep(3)
                # chan.send(server_key + "\n")
                # time.sleep(4)
                # print("executing general command on server")
                # chan.send("ver"+"\n")
                # time.sleep(2)
                # resp = chan.recv(9999)
                # output = resp.decode('ascii').split(',')
                # print(''.join(output))
                # print("executing shutdown command")
                # chan.send("shutdown /s /f" + "\n")
                # print("Waiting for 5 mins to shutdown completely and then try connection  if it is alive or not")
                # time.sleep(300)
                # print("Checking for server connection again to test if shutdown is successful")
                # chan.send(command_ssh + "\n")
                # if chan.recv_stderr() == False:
                #     print("Server is still on. Try again")
                # else:
                #     print("Shutdown successful")
            except Exception as e:
                print(HTTPStatus.INTERNAL_SERVER_ERROR.value)
        except Exception as err:
            print(HTTPStatus.BAD_REQUEST.value)
    except Exception as e:
        print(HTTPStatus.UNAUTHORIZED.value)


server_shutdown()