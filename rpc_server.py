from xmlrpc.server import SimpleXMLRPCServer
import random
import os
import fcntl #file control module
import time 
import subprocess as s

def update_servers(s1, host_list):
    delete_str = "sed -i \'/" + s1 + "/d\' server.txt"
    #s.check_output("sed -i \'/" + s1 + "/d\' server.txt" , shell=True)
    s.check_output(delete_str , shell=True)
    newstr = "echo " + s1 + "=" + host_list[0] + "=" + str(host_list[1]) + ">> server.txt"
    print(newstr)
    s.check_output(newstr,shell=True)

def get_free_host():
    lines=[]
    found_host=[-1,"","No MORE FREE SLOTS"]
    with open("server.txt") as f:
         lines = f.read().splitlines()
    servers={}
    for i in lines:
        l1=i.split("=",1)
        servers[l1[0]] = l1[1]
    host_list=[]
    for keys in sorted(servers):
        host_list = servers[keys].split("=")
        host_list[1] = int(host_list[1])
        if host_list[1] < 4:
           host_list[1] = host_list[1]+1
           found_host[0]=0
           found_host[1]=host_list[0]
           found_host[2] = "Slots Left = " + str(4 - host_list[1])
           update_servers(keys,host_list)
           break;
    return found_host;

def delete(server):
    res = s.check_output('grep '+ server + ' server.txt',shell=True).decode('utf-8').rstrip("\n")
    l1 = res.split('=')
    l1[2]=int(l1[2])
    if l1[2] > 0:
      l1[2] = l1[2]-1
      s.check_output("sed -i \'/" + server + "/d\' server.txt",shell=True)
      newstr="echo " + l1[0]+ "="+ l1[1] + "=" + str(l1[2]) + ">> server.txt"
      s.check_output(newstr,shell=True)
      print("Deleted the used lot")
    else:
      print("Nothing To Delete Count is already Zero")

    return l1

def delete_function(server):
     try:
        #try/except in case the file is still locked by another process
        #open the file for editing
        with open('/home/kairos/Cluster/swarm/SCHEDULER/lock.txt', 'a') as myfile:
            #lock the file
            print("TRYING FOR THE LOCK DELETE FUNCTION")
            fcntl.flock(myfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
            print("GOT THE LOCK in  DELETE FUNCTION")
            #edit it
            myfile.write('Hello World\n')
            val = delete(server)
            time.sleep(1)
            #print_server()
            #and now unlock it so other processed can edit it!
            fcntl.flock(myfile, fcntl.LOCK_UN)
            return val
     except Exception as e:
        print(f"No idea what happened: {e!r}")
 #    except :
       #wait before retrying
        print("GOT EXCEPTION\n")
        time.sleep(0.05)


def get_function():
    # we keep trying forever until we manage to access the file
    # you can change the loop to try a certain number of times     
     try:
        #try/except in case the file is still locked by another process 
        #open the file for editing  
        with open('/home/kairos/Cluster/swarm/SCHEDULER/lock.txt', 'a') as myfile: 
            #lock the file   
            print("TRYING FOR THE LOCK")
            fcntl.flock(myfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
            print("GOT THE LOCK")
            myfile.write('Hello World\n')
            val = get_free_host()
            time.sleep(1)
            #and now unlock it so other processed can edit it!           
            fcntl.flock(myfile, fcntl.LOCK_UN)
            print("UNLOCKED")
            return val
     except Exception as e:
        print(f"No idea what happened: {e!r}")
 #    except :
       #wait before retrying  
        print("GOT EXCEPTION\n")
        time.sleep(0.05)

#server = SimpleXMLRPCServer(('localhost',3000),logRequests=True,allow_none=True)
server = SimpleXMLRPCServer(('0.0.0.0',3000),logRequests=True)


server.register_function(get_function)
server.register_function(delete_function)
#server.register_function(get_free_host)

if __name__ == '__main__':
  try:
     print('Serving The Rpc Requests')
     server.serve_forever()
  except KeyboardInterrupt:
     print('Exiting ...')


	
