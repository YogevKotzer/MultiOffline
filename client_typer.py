import socket
from pynput.keyboard import Key, Controller, Listener
import sys
import readchar
import threading




SERVER_IP = "10.10.3.243" # reset these
SERVER_PORT = 700 # reset these for user
keyboard = Controller()
my_key = []

def trim(s):
	if(s.startswith("<")):
		s = s[1:s.find(":")]
	return s
	
	
def listen():
	# Collect events until released
	with Listener(on_press=on_press, on_release=on_release) as listener: 
		listener.join()

def on_press(key):
	global my_key
	#print(str(key))
	##print('{0} pressed'.format(key))
	
	temp = trim(str(key))
	temp = repr(temp)
	my_key += [temp]
	
def on_release(key):
	global my_key
	##print('{0} release'.format(key))
	if key == Key.esc:
		# Stop listener
		return False
	key = trim(str(key))
	my_key += ["res" + key]
	#print ("new res key", key)
	
		
threads = []
t = threading.Thread(target=listen)
threads.append(t)
t.start()


def main():
	global my_key
	global SERVER_IP
	global SERVER_PORT
	a = open("client.config",'r').read().split('\n')
	if(SERVER_IP == ""):
		SERVER_IP = a[0][a[0].find("=") + 1]
	if(SERVER_PORT == 0):
		SERVER_PORT = int(a[1][a[1].find("=") + 1])
	old_key = 0
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connecting to remote computer 80
	server_address = (SERVER_IP, SERVER_PORT)
	sock.connect(server_address)

	# Sending data to server
	msg = "connected!_client"
	sock.sendall(msg.encode())

	# Receiving data from the server
	server_msg = sock.recv(1024)
	server_msg = server_msg.decode()

	print(server_msg)
	last_msg = 0
	new_msg = 0
	inp = ""
	
	while(my_key != "0"):
		if(my_key != []):
			curr = my_key[0]
			if(curr.startswith("res")):
				new_msg = (curr + "\x15").encode()
			else:
				inp = curr
				new_msg = (inp + "\x15").encode()
			#print(curr)
			old_key = curr
			sock.sendall(new_msg)
			my_key = my_key[1:]
		# Closing the socket
	sock.close()

main()