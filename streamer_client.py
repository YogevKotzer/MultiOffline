from socket import socket
from zlib import decompress

import pygame

WIDTH = 1900
HEIGHT = 1000
SERVER_IP = '192.168.1.20'
SERVER_PORT = 5000


def recvall(conn, length):
	""" Retreive all pixels. """

	buf = b''
	while len(buf) < length:
		data = conn.recv(length - len(buf))
		if not data:
			return data
		buf += data
	return buf


def main():
	global SERVER_IP
	global SERVER_PORT
	a = open("client.config",'r').read().split('\n')
	if(SERVER_IP == ""):
		SERVER_IP = a[0][a[0].find("=") + 1]
	if(SERVER_PORT == 0):
		SERVER_PORT = int(a[1][a[1].find("=") + 1])
	
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	clock = pygame.time.Clock()
	watching = True

	sock = socket()
	sock.connect((SERVER_IP, SERVER_PORT))
	try:
		while watching:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					watching = False
					break

			# Retreive the size of the pixels length, the pixels length and pixels
			size_len = int.from_bytes(sock.recv(1), byteorder='big')
			size = int.from_bytes(sock.recv(size_len), byteorder='big')
			pixels = decompress(recvall(sock, size))

			# Create the Surface from raw pixels
			img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')

			# Display the picture
			screen.blit(img, (0, 0))
			pygame.display.flip()
			clock.tick(60)
	finally:
		sock.close()


if __name__ == '__main__':
	main()