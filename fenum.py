import socket 
import random
from queue import Queue
from colorama import Fore 
import sys
import argparse 
import re
    
def main ():
    parser = argparse.ArgumentParser(description="""Fenum - file enumerator with
                                     search capability.""")
    parser.add_argument("-U" , "--username" , dest="username", action="store",
                        default="anonymous" , help="FTP username ")
    parser.add_argument("-P" , "--password", dest="password", action="store",
                        default="", help="FTP password ")
    parser.add_argument("-r" , "--remote-host", dest="rhost", action="store",
                        required=True , help="FTP server IP address")
    parser.add_argument("-p" , "--port" , dest="port", action="store",
                        type=int, default=21, help="FTP port - default is 21")
    parser.add_argument("-l" , "--local-host" , dest="lhost", action="store",
                        required=True, help="localhost interface IP address to create data connection")
    parser.add_argument("-t" , "--path" , dest="path", action="store",
                        default="", help="path to start enumeration - default is '/'")
    parser.add_argument("-s" , "--search", dest="search", action="store",
                        help="STRING to search in FTP files")
    parser.add_argument("-e" , "--regex", dest="regex", action="store",
                        help="regex to search in FTP files")
    arguments = parser.parse_args()

    
    control_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM) 
    control_socket.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
    
    login(control_socket, arguments.rhost, arguments.port, arguments.username, 
          arguments.password)
    result = enumerator(control_socket,arguments.lhost, arguments.path)
    
    
    if arguments.search :
        search(arguments.search , result)
    elif arguments.regex : 
        reg_search(arguments.regex , result)
    else : 
        for k , v in result.items() :
          print (Fore.BLUE + k + "\n")
          for f in v : 
              print (Fore.RED + f + "\n")
    
        
def login (control_socket, rhost, port=21, user="anonymous", password=""):
    try: 
        control_socket.connect((rhost , port))
        data = control_socket.recv(1024).decode()
    except Exception as e : 
        print (e)
        
    msg = ("USER %s" %(user) + "\r\n")
    control_socket.sendall(msg.encode())
    data = control_socket.recv(1024).decode() 
    msg = ("PASS %s" %(password) + "\r\n")
    control_socket.sendall(msg.encode())
    data = control_socket.recv(1024).decode()
    if "230" in data : 
        print ("[+] Logged in ... ")
    else : 
        print ("[-] Wrong credentials! ")
        print (data)
        sys.exit(1)
        
    
def enumerator(control_socket, lhost, path):
    directories = Queue()
    directories.put(path)
    
    result = {}
    
    print ("[+] Creating Data Connection")
    
    while not directories.empty() : 

        try: 
            data_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
            data_socket.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1 )
            data_socket.settimeout(10)
            DATA_PORT = random.randint(50000 , 60000)
            data_socket.bind((lhost , DATA_PORT))
            P2 = DATA_PORT%256
            P1 = int((DATA_PORT-P2)/256)
            data_socket.listen(1)
        except Exception as e : 
            print (e)
        host = lhost.split(".")
        msg = ("PORT %s,%s,%s,%s,%s,%s" %(host[0], host[1], host[2],
                                          host[3] , str(P1), str(P2))+ "\r\n")
        try :
            control_socket.sendall(msg.encode())
            data = control_socket.recv(1024).decode()
        except Exception as e: 
            print (e)
            continue
        try : 
            server_data , addr = data_socket.accept()
        except Exception as e:
            print(e)
            continue
        
        path = directories.get()
        print (path)
        msg = ('NLST -la %s' %(path) + "\r\n").encode()
        
        control_socket.sendall(msg)
        while 1:
            data = server_data.recv(1024).decode()
            server_data.close()
            break
        while 1:
            c_data = control_socket.recv(1024).decode()
            break
        
        #print (c_data , data)
        for line in str(data).split("\n"): 
            if "DIR" in line: 
                directories.put(path+"/"+" ".join(line.split(" ")[19:]).rsplit("\r")[0])
            elif line.split(" ")[3:]:
                file_name = " ".join((" ".join(line.split(" ")[3:]).rstrip("\r").lstrip()).split(" ")[1:])
                if path in result : 
                  result[path].append("\t\t\t"+file_name)
                else : 
                    result.update([(path ,["\t\t\t"+file_name])])
           
    return result

def search(s , r) : 
    print ("Search Result : ")
    for k , v in r.items() : 
        for f in v : 
            if s in k or s in f : 
                print (k , f)
                
def reg_search (reg , r) : 
    print (reg)
    print ("Regex Search Result : ")
    for k , v in r.items() : 
        for f in v : 
            m = re.match(reg , f.lstrip("\t\t"))
            n = re.match(reg , k)
            if m or n : 
                print (k , f)
        
    
if __name__ == "__main__" : 
    main()
