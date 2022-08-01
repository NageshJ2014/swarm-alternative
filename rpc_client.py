from xmlrpc.client import ServerProxy
import sys

proxy = ServerProxy('http://localhost:3000')

if __name__ == '__main__':
    if sys.argv[1] == "Create":
      #print(proxy.time_function())
      print(proxy.get_function())
    elif sys.argv[1] == "Delete":
      print(proxy.delete_function(sys.argv[2]))
