from colorama import Fore, Back, Style
from datetime import datetime
import multiprocessing
import colorama
import argparse
import socket
import time
import os

colorama.init()
if(os.name == "nt"):
    os.system("cls")
else:
    os.system("clear")

def time():
    info = datetime.today()
    time = datetime.ctime(info)
    return time

def scan_ports(target_host):
    open_ports = []    
    for port in range(1, 65536):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Zaman aşımını 1 saniye olarak ayarlayabilirsiniz
        try:
            result = sock.connect_ex((target_host, port))
          
            if result == 0:
                open_ports.append(port)
        except Exception as e:
            print("Hata -> " + str(e))  
        finally:
            sock.close()
    
    return open_ports

def scanPort(host,port,timeout):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)            
        s.settimeout(timeout)
        s.connect((host,port))
        response_service = s.recv(1024)
        #print(f"{Fore.YELLOW} port {port} -> {Fore.GREEN} açık")           
        print(f"{Fore.YELLOW} Port {port} -> {Fore.GREEN} Açık {Fore.BLUE} -> ({response_service.decode()})")

    except ConnectionRefusedError as c:
        print(f"{Fore.YELLOW} Port {port} -> {Fore.RED} Kapalı -> ({str(c)})")
        pass
    except socket.timeout as t:
        if(port == 80):
            httpMessage = "GET / HTTP/1.0\r\n\r\n"
            s.send(httpMessage.encode())
            httpRecv = s.recv(1024)
            print(f"{Fore.YELLOW} Port {port} -> {Fore.GREEN} Açık {Fore.WHITE} -> \n\n({httpRecv.decode()}\n\n)")
        else:
            print(f"Zaman aşımı ({timeout} saniye) süresi içinde bağlantı kurulamadı. Timeout süresini arttırmayı deneyin. -> ({str(t)})")
    except Exception as e:
        print("Hata ->" + e)
    finally:
        s.close()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--host", required=True, help="target host")
ap.add_argument("-p", "--port",required=False,help="target port")
ap.add_argument("-t", "--timeout",required=True,help="scan timeout")

args = vars(ap.parse_args())

port = args["port"]
host = args["host"]
timeout = args["timeout"]

try:
    if(port is None):
        open_ports = scan_ports(host)
        print("Açık olan portlar:")
        for port in open_ports:
            print(port)

    elif("-" in port):
        split_data = port.split("-")
        f1 = int(split_data[0].strip())
        f2 = int(split_data[1].strip())

        print(Fore.RED)
        start_time = time()
        print("Start Time -> " + start_time + "\n====================\n\n")
        
        
        for i in range(f1,f2 +1):
            scanPort(host,i,int(timeout))
        print(Fore.RED)
        end_time = time()
        print("\n\nEnd Time -> " + end_time+"\n====================")
        
    else:
        print(Fore.RED)
        start_time = time()
        print("Start Time -> " + start_time + "\n====================\n\n")
        try:
            port_num = int(port)
            scanPort(host,port_num,int(timeout))        
            end_time = time()
            print(Fore.RED) 
            print("\n\nEnd Time -> " + end_time+"\n====================")
        except ValueError:
            print("Geçersiz port numarası. Tek bir port numarası veya port aralığı belirtiniz.")
except KeyboardInterrupt:
    end_time = time()
    print("End Time -> " + end_time)
    print("\nbye bye")