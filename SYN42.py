#!/usr/bin/python

#SYN42 - Multi-Threaded TCP SYN Port Scanner
#Version 1.2
#Author: Jacob Holcomb/Gimppy - Security Analyst
#Date: December 2012
#http://infosec42.blogspot.com

from scapy.all import *
from socket import inet_aton, inet_ntoa
from time import sleep
from sys import argv
import thread
import Queue



scannedPorts = []
openPorts = []
timeOports = []
work2do = Queue.Queue()


def targServer():

	while True:
	
		try:
			server = inet_aton(raw_input("\n[*] Please enter the IPv4 address of the server you would like to SYN scan:\n\n>"))
			server = inet_ntoa(server)
			break

		except:
			print "\n\n[!!!] Error: Please enter a valid IPv4 address. [!!!]\n\n"
			sleep(1)
			continue
			
	return server		


def portRange():

	while True:
	
		chPorts = raw_input("\n[*] Please choose one of the following. [*]\n\n    1. Scan specific ports\n    2. Scan range of ports\n\n>")
		startPort = None
		endPort = None
		selectPort = None
		
		if chPorts == "1":
			
			portRange = []
			
			while True:
			
				proceed = None
				contin = None
				
				try:
					addPort = raw_input("\n[*] Please enter a port you would like to scan on host:\n\n>")
					if int(addPort) > 65535:
						print "\n[!!!] Port must be less than 65535 [!!!]"
						sleep(1)
						
					elif int(addPort) < 1:
						print "\n[!!!] Port must be greater than 1 [!!!]"
						sleep(1)
						
					else:	 	 
						portRange.append(int(addPort))
						print "\n\n    --Selected ports: %s\n" % portRange
						
				except:
					print "\n\n[!!!] ERROR: Ports need to be integers. [!!!]\n\n"
					sleep(1)
					continue		
					
				while proceed != "yes" and proceed != "no":
					proceed = raw_input("\n[*] Would you like to add another port to the scan list? Please enter \"yes\" or \"no\"\n\n>")
					
					#if proceed == "yes":
					#	break

					if proceed == "no":
						print "\n\n[!!!] You selected ports %s. [!!!] \n" % portRange
						sleep(1)
							
						while contin != "yes" and contin != "no":
								
							contin = raw_input("\n[*] Proceed to scan with selected ports? Please enter \"yes\" or \"no\"\n\n>")
					elif proceed != "yes" and proceed != "no":
						print "\n\n[!!!] Error: You entered %s. Please enter \"yes\" or \"no\"! [!!!]\n\n" % proceed
						contin = None
						sleep(1)
				
				if contin == "yes":
					selectPort = portRange
					break
					
				else:
					continue		
			
		elif chPorts == "2":
			
			while True:
				try:
					startPort = raw_input("\n[*] Please enter the starting port you would like to scan on host:\n\n>")

					if int(startPort)  > 65535:
						print "\n[!!!] Starting port must be less than 65535 [!!!]"
						sleep(1)
							
					elif int(startPort) < 1:
						print "\n[!!!] Starting port must be greater than 1 [!!!]"
						sleep(1)
						
					else:	
						sPort = int(startPort)	
						
					endPort = raw_input("\n[*] Please enter ending port you would like to scan on your host:\n\n>")	
						
					if int(endPort) > 65535:
						print "\n[!!!] Ending port must be less than 65535 [!!!]"
						sleep(1)
						
					elif int(endPort) < 1:
						print "\n[!!!] Ending port must be greater than 1 [!!!]"
						sleep(1)
							
					else:	
						ePort = int(endPort)
						ePort += 1
						
					portRange = range(sPort,ePort)
					break
		
				except:
					print "\n\n[!!!] ERROR: Ports need to be integers. [!!!]\n\n"
					sleep(1)
					continue	
			break
		
		else:
			print "\n\n[!!!] Please choose option 1 or 2. [!!!]\n\n"
			sleep(1)
			continue
		break		
	
	return portRange, startPort, endPort, selectPort		
	
		
def slaveLabor():
	
	while True:
		
		numThread = raw_input("\n\n[*] How many slave thread's would you like to use in your scan. Please enter a number 1-100:\n\n>")
			
		try:
			int(numThread)
			
			if int(numThread) > 100:
				print "\n\n[!!!] ERROR: Please enter a number less than or equal to 100. [!!!]\n"
				sleep(1)
			
			elif int(numThread) < 1:
				print "\n\n[!!!] ERROR: Please enter a number greater than 1. [!!!]\n"
				sleep(1)
			
			else:
				break		
		
		except:
			print "\n\n[!!!] ERROR: Thread count must be an integer [!!!]\n\n"
			sleep(1)
			continue			
		
	return range(int(numThread))
	
	
def scan(server):
			 
	while True:
		
		try:
			curPort = work2do.get(timeout=.5)
			print "\r    [!!!] Scanning TCP port %d.\r" % curPort
				
		except:
			return
			
				
		#Creating IP Packet 		
		host = server
		ipPakt = IP()
		ipPakt.dst = host
		tcp = TCP()
		tcp.dport = curPort
		tcp.sport = 1337
		tcp.flags = "S"
		
		try:
			paktResp = sr1(ipPakt/tcp, verbose=False, timeout=.5)
		
			if paktResp is None:
				print "\r    [-] Port %d: timed out. Did not receive a response" % curPort
				timeOports.append(curPort)
			
			elif paktResp[TCP].flags == 18:
				print "\r    [*] Port %d: OPEN. Received SYN/ACK" % curPort
				openPorts.append(curPort)
		
			elif paktResp[TCP].flags != 18:
				print "\r    [-] Port %d CLOSED. Did not receive SYN/ACK" % curPort
			
				
                except:
                	print "[---] Thread error. Terminating thread and queing threads workload. [---]"
                	work2do.put(curPort)
                	work2do.task_done()
                	return
                
                scannedPorts.append(curPort)	
                work2do.task_done()

def main():

	proceed = None
	server = targServer()
	ports, startPort, endPort, selectPort = portRange()
	
	for port in ports:
		work2do.put(port)
		
	labor = slaveLabor()	
		
	while proceed != "yes" and  proceed != "no":
		
		sleep(.5)
		print "\n\n[!!!] SYN Scan Settings: [!!!]\n\n    [*] Target: %s\n    [*] Port Range: %s - %s\n    [*] Selected Ports: %s\n    [*] Slave Thread's: %s\n\n" % (server, startPort, endPort, selectPort, len(labor))
		proceed = raw_input("\n[*] Would you like to continue with the TCP SYN scan? Please enter \"yes\" or \"no\"\n\n>")
		
		if proceed == "yes":
			
			print "\n\n[!!!] Initiating TCP SYN Scan. Press ctrl + c or z to cancel! [!!!] \n\n"
			sleep(2)
				
			try:
			
				for slave in labor:
					thread.start_new_thread(scan,(server,))
				
			except:
				return
			
		elif proceed == "no":
			print "\n\n[!!!] SYN scan cancelled. You are now exiting %s [!!!]\n\n" % sys.argv[0] 
			sys.exit(0)

		else:
			print "\n\n[!!!] Error: You entered %s. Please enter \"yes\" or \"no\"! [!!!]\n\n" % proceed			
		

	work2do.join()	
	print "\n\n[!!!] TCP SYN scan complete. %d ports were scanned. %d open ports, %d closed ports, and %d ports timed out. [!!!]\n" % (len(scannedPorts), len(openPorts), len(scannedPorts) - len(openPorts) - len(timeOports), len(timeOports))
	print "    --SCAN RESULTS for %s--\n\n    [*] Open Ports: %s\n" % (server, openPorts)
	
	
#Top-level script environment

if __name__ == "__main__":

    main() 

