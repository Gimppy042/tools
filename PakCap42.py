#!/usr/bin/env python

import socket, struct, binascii, signal, os
from time import sleep


class Capture:

	count = 1

	def __init__(self):
	
		pass
	
		
	def sigHandle(self, signum, frm): # Signal handler
	
		print "\n[!!!] Closing capture socket and shutting down [!!!]\n"
		sleep(1)
			
	#Create File
	def fileCreate(self):
		
		print "\n[*] Your current file directory is %s. " % os.getcwd()

		try:
			File = raw_input("[*] Please provide a name for the capture file:\n>")
			fileOpen = open(File, "a")
			print "\n[*] Capture file %s will be written to %s." % (File, os.getcwd())
			return fileOpen 	
			   
		except:
			print "\n[*] ERROR! There was an issue creating your file. Please make sure you have write access to %s!!!!!\n" % os.getcwd()         


	def RawSock(self):

		try:
			#PF_Packet = packet interface. htons() tells the kernel what protocol we want.
			rawSock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800)) #/usr/include/linux/if_ether.h
			print "[*] Created socket for 802.3 Ethernet Packet.\n[*] Using Ethernet Protocol ID 0x0800 Internet Protocol"
			return rawSock
			
		except:
			print "\n[!!!] There was an error creating the socket object [!!!]\n"	
			
			
	def PktRecv(self, rawSock):
	
		try:
			capPkt = rawSock.recvfrom(2048)# Recv data from socket
			return capPkt
			
		except:		
			capPkt.close()
			print "\n[!!!] There was an error capturing data on the socket object [!!!]\n"
			
			
	def ParsePkt(self, capPkt, capFile, capFilter):
	
		#Add logic to look for 802.1q Vlan/Trunk Tag in Layer 2
		#Add logic to look for IP Options in Layer 3
		#Add logic to look for TCP Options in Layer 4 if protocol is TCP
		try:
			File = capFile
			Filter = capFilter		
			#Breaking up the packet
			ethHdrPkd = capPkt[0][0:14] #Packed Layer 2 ethernet header
			ipHdrPkd = capPkt[0][14:34] #Packed Layer 3 IP header
			tprtHdrPkd = None #Packed Layer 4 Transport Layer header.
			tprtProto = None
			appHdr = None
			appHdrHex = None
			
			#Creating parseable tuple's
			ethHdr = struct.unpack(">6s6s2s", ethHdrPkd)
			ipHdr = struct.unpack(">1s1s2s2s2s1s1s2s4s4s", ipHdrPkd)
			
			if binascii.hexlify(ipHdr[6]) == "06":#TCP Protocol Number
				tprtHdrPkd = capPkt[0][34:54] #Packed Layer 4 Transport Layer header.
				appHdr = capPkt[0][54:]
				appHdrHex = binascii.hexlify(capPkt[0][54:])
				tprtHdr = struct.unpack(">HHLLBBHHH", tprtHdrPkd)
				tprtProto = "TCP"	
				
			elif binascii.hexlify(ipHdr[6]) == "11":# UDP Protocol Number
				tprtHdrPkd = capPkt[0][34:42] #Packed Layer 4 Transport Layer header.
				appHdr = capPkt[0][42:]
				appHdrHex = binascii.hexlify(capPkt[0][42:])
				tprtHdr = struct.unpack(">HHHH", tprtHdrPkd)
				tprtProto = "UDP"
					
			#Creating Human Redable Data
			dstMac = binascii.hexlify(ethHdr[0]) #dst mac hex
			srcMac = binascii.hexlify(ethHdr[1]) #src mac hex
			dstMac = ":".join(["%s%s" % (dstMac[nib], dstMac[nib+1]) for nib in range(0,12,2)])
			srcMac = ":".join(["%s%s" % (srcMac[nib], srcMac[nib+1]) for nib in range(0,12,2)]) 
			ethType = binascii.hexlify(ethHdr[2]) #ether type
			srcIp = socket.inet_ntoa(ipHdr[8]) #src ip
			dstIp = socket.inet_ntoa(ipHdr[9]) #dst ip
				
			File.write("\n" + "_" * 65 + "\n[!!!] Start of packet #%d [!!!]\n" % self.count)
			File.write("\n\t[--] Layer 2 [--]\n\n[*] Source Mac: %s\n[*] Destination Mac: %s\n[*] Ethernet Type: 0x%s\n" % (srcMac, dstMac, ethType))
			File.write("\n\t[--] Layer 3 [--]\n\n[*] Source IP: %s\n[*] Destionation IP: %s\n" % (srcIp, dstIp))
			
			if tprtProto != None:
				srcPort = tprtHdr[0]
				dstPort = tprtHdr[1]
				File.write("\n\t[--] Layer 4 [--]\n\n[*] Protocol: %s\n[*] Source Port: %s\n[*] Destionation Port: %s\n" % (tprtProto, str(srcPort), str(dstPort)))
				
				if tprtProto == "TCP":
					seqNum = tprtHdr[2]
					ackNum = tprtHdr[3]
					offset = tprtHdr[4]
					flag = tprtHdr[5]
					window = tprtHdr[6]
					chksum = tprtHdr[7]
					File.write("[*] Sequence #: %s\n[*] Acknowledgement #: %s\n[*] Offset: %s\n[*] Flag: %s\n" % (str(seqNum), str(ackNum), str(offset), str(flag)))
					File.write("\n\t--Flag Values--\n\tFIN = 1 (0x1)\n\tSYN = 2 (0x2)\n\tRST = 4 (0x4)\n\tPSH = 8 (0x8)\n\tACK = 16 (0x10)\n\tURG = 32 (0x20)\n\n")
					File.write("[*] Window Size: %s\n[*] Checksum %s\n" % (str(window), str(chksum)))
					
				elif tprtProto == "UDP":
					length = tprtHdr[2]
					chksum = tprtHdr[3]
					File.write("[*] Length: %s\n[*] Checksum %s\n" % (str(length), str(chksum)))
					
			else:
				File.write("\n\t[--] Layer 4 [--]\n\n[!!!] Packet is not TCP or UDP\n")
			
			
			if Filter != None:
				if int(srcPort) == int(Filter) or int(dstPort) == int(Filter):
					File.write("\n\t[--] Data [--]\n\n[*] Raw Data:\n\n%s\n\n[*] Hex Dump:\n\n %s" % (str(appHdr), str(appHdrHex)))
				
				else:
					File.write("\n\t[--] Data [--]\n\n[*] Port filter not met. Data will not be printed.\n")
			else:
				File.write("\n\t[--] Data [--]\n\n[*] Raw Data:\n\n%s\n\n[*] Hex Dump:\n\n %s" % (str(appHdr), str(appHdrHex)))
				
		except:
			print "\n[!!!] Error parsing and breaking up the captured packet [!!!]\n"			
			
def main():			
	
	#Ask user if they want to do timed packet capture.	
	viewPkt = Capture()
	capFile = viewPkt.fileCreate()
	sock = viewPkt.RawSock()
	capFilter = None
	count = 0
	signal.signal(signal.SIGINT, viewPkt.sigHandle) #Setting signal handler for ctrl + c
	
	contin = raw_input("\n[*] Would you like to add a port filter for data capture?\n>")
	
	while contin != "yes" and contin != "no":
		print "\n[!!!] Please answer with \"yes\" or \"no\". [!!!]\n"
		sleep(1)
		contin = raw_input("\n[*] Would you like to add a port filter for data capture?\n>")
		
	if contin == "yes":
		while True:
			capFilter = raw_input("\n[*] Please enter a port number ranging from 1-65535?\n>")
			
			try:
				if int(capFilter)  > 65535:
					print "\n[!!!] Starting port must be less than 65535 [!!!]"
					sleep(1)
							
				elif int(capFilter) < 1:
					print "\n[!!!] Starting port must be greater than 1 [!!!]"
					sleep(1)
						
				else:	
					print "\n[*] Only data matching port filter %s will be written to file. [*]" % capFilter
					sleep(1)
					break
			except:
				print "\n\n[!!!] ERROR: Ports need to be integers. [!!!]\n\n"
				sleep(1)
				continue
						
	elif contin == "no":
		capFilter = None
		print "\n\n[!!!] No port filter was chosen. All data will be written to file [!!!]\n"
		sleep(1)
		
	print "[*] Preparing to capture packets. Press ctrl + c to exit. [*]\n"
	sleep(2)
		
	while True:
	
		try:
			pkt = viewPkt.PktRecv(sock)
			viewPkt.ParsePkt(pkt, capFile, capFilter)
		
		except:
			break
			
		count += 1
		Capture.count += 1
		print "[*] Number of packets captured: %d" % count				
			
#Top-level script environment

if __name__ == "__main__":

    main()			
    		
