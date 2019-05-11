import socket
from pynput.keyboard import Key, Controller
import os
import readchar
import threading
import sys
import time

s_data = {'Key.alt':Key.alt,'Key.alt_l':Key.alt_l,'Key.alt_r':Key.alt_r,'Key.backspace':Key.backspace,'Key.caps_lock':Key.caps_lock,'Key.cmd':Key.cmd,'Key.cmd_r':Key.cmd_r,'Key.ctrl':Key.ctrl,'Key.ctrl_l':Key.ctrl_l,'Key.ctrl_r':Key.ctrl_r,'Key.delete':Key.delete,'Key.down':Key.down,'Key.end':Key.end,'Key.enter':Key.enter,'Key.esc':Key.esc,'Key.f1':Key.f1,'Key.f10':Key.f10,'Key.f11':Key.f11,'Key.f12':Key.f12,'Key.f13':Key.f13,'Key.f14':Key.f14,'Key.f15':Key.f15,'Key.f16':Key.f16,'Key.f17':Key.f17,'Key.f18':Key.f18,'Key.f19':Key.f19,'Key.f2':Key.f2,'Key.f20':Key.f20,'Key.f3':Key.f3,'Key.f4':Key.f4,'Key.f5':Key.f5,'Key.f6':Key.f6,'Key.f7':Key.f7,'Key.f8':Key.f8,'Key.f9':Key.f9,'Key.home':Key.home,'Key.insert':Key.insert,'Key.left':Key.left,'Key.menu':Key.menu,'Key.num_lock':Key.num_lock,'Key.page_down':Key.page_down,'Key.page_up':Key.page_up,'Key.pause':Key.pause,'Key.print_screen':Key.print_screen,'Key.right':Key.right,'Key.scroll_lock':Key.scroll_lock,'Key.shift':Key.shift,'Key.shift_r':Key.shift_r,'Key.space':Key.space,'Key.tab':Key.tab,'Key.up':Key.up}
LISTEN_PORT = 700
keyboard = Controller()
flag = True
threads = {}

def handle_msg(msg):
	global threads
	if(msg.count("'") > 1):
		msg = msg.replace("'", "")
	if(msg.count('"') > 1):
		msg = msg.replace('"', '')
	#print(msg,"fuck you")
	if(msg.startswith("res")):
		#print (msg)
		threads.pop(msg[msg.find("res") + 3:])
	elif(msg.startswith("Key")):
		t = threading.Thread(target=s_press, args=[msg])
		threads[msg] = t
		t.start()
		#print(msg, "new key!")
	elif(len(msg) == 1):
		t = threading.Thread(target=press, args=[msg[0]])
		threads[msg[0]] = t
		t.start()
		#print(msg, "new key!")
	else:
		print("shit", msg,"sex")

#special key press
def s_press(char):
	global threads
	global keyboard
	while(char in threads.keys()):
		keyboard.press(s_data[char])
		time.sleep(0.1)
		#print("pressed", char)
		keyboard.release(s_data[char])


def press(char):
	global threads
	global keyboard
	while(char in threads.keys()):
		keyboard.press(char)
		time.sleep(0.1)
		#print("pressed", char)
		keyboard.release(char)


		
def print_keys():
	global threads
	global flag
	while(flag):
		time.sleep(1)
		print (threads.keys())

t = threading.Thread(target=print_keys)
threads["status"] = t
t.start()

def main():
	global threads
	global keyboard
	global s_data
	# Create a TCP/IP socket
	listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Binding to local port 80
	server_address = ('', LISTEN_PORT)
	listening_sock.bind(server_address)

	# Listen for incoming connections
	listening_sock.listen(1)

	# Create a new conversation socket
	client_soc, client_address = listening_sock.accept()

	# Receiving data from the client
	client_msg = client_soc.recv(1024)
	client_msg = client_msg.decode()

	# Sending data back
	msg = "connected!_s"
	client_soc.sendall(msg.encode())
	print(client_msg)
	old_key = 0
	
	while(client_msg != ""):
		client_msg = client_soc.recv(1024)
		client_msg = client_msg.decode()
		#print(client_msg, len(client_msg))
		msg = str(client_msg)
		msg = msg.split("\x15")
		msg = msg[:-1]
		for x in msg:
			(threading.Thread(target=handle_msg,args=[x])).start()
	# Closing the conversation socket
	client_soc.close()


	# Closing the listening socket
	listening_sock.close()

try:
	main()
except:
	flag = False
flag = False