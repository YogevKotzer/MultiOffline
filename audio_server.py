import pyaudio
import socket
from threading import Thread
CLIENT_IP = '127.0.0.1'
CLIENT_PORT = 12345


frames = []

def udpStream():
	global CLIENT_IP
	global CLIENT_PORT
	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	

	while True:
		if len(frames) > 0:
			udp.sendto(frames.pop(0), (CLIENT_IP,CLIENT_PORT))

	udp.close()

def record(stream, CHUNK):	
	while True:
		frames.append(stream.read(CHUNK))

def main():
	global CLIENT_IP
	global CLIENT_PORT
	
	a = open("server.config",'r').read().split('\n')
	if(CLIENT_IP == ""):
		CLIENT_IP = a[0][a[0].find("=") + 1]
	if(CLIENT_PORT == 0):
		CLIENT_PORT = int(a[1][a[1].find("=") + 1])
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 2
	RATE = 44100

	p = pyaudio.PyAudio()

	stream = p.open(format = FORMAT,
					channels = CHANNELS,
					rate = RATE,
					input = True,
					frames_per_buffer = CHUNK,
					)

	Tr = Thread(target = record, args = (stream, CHUNK,))
	Ts = Thread(target = udpStream)
	Tr.setDaemon(True)
	Ts.setDaemon(True)
	Tr.start()
	Ts.start()
	Tr.join()
	Ts.join()
	
main()