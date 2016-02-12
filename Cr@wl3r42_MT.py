#!/usr/bin/env python

# Cr@wl3r42 v1.0
# C0d3d by Gimmpy/Jacob Holcomb
# March 2013

from bs4 import BeautifulSoup # Version 4
from time import sleep
from sys import exit
import urllib2, Queue, base64, signal, os, threading

work2do = Queue.Queue()
httpRequest = None
allLinks = []
new_count = 0
discov_count = 0


class clientThread(threading.Thread): #Subclass of threading.thread
    
    def __init__(self, Links, website, _type):
    
        threading.Thread.__init__(self)
        self.Links = Links
        self.website = website
        self._type = _type


    def run(self): #Overriding parent class method
    
		global new_count
		global discov_count
	
		for link in self.Links:
	
			try:
				link = link[self._type]
			
				if link.find(self.website) != -1 or "http:" not in link[0:5]:
					if "//" in link[0:2]:
						link = "http:" + link
					elif "/" in link[0:1]:
						link = self.website + link		
					else:
						link = "%s" % link
					
				if link.endswith(".") == True:
					link = link.rstrip(".")			
				
				if link not in allLinks and link.find(self.website) != -1:	
					try:
						str(link)
						if link.endswith(("pdf", "ppt", "gif", "jpg", "png")) == False:
							work2do.put(link)
						allLinks.append(link)
						new_count += 1
					except:
						pass
						
					print "[*] Newly Discovered URL.\n[*] URL: %s\n[*] Total unique URLS %d\n" % (link, new_count)
				else:
					discov_count += 1	
			
			except(KeyError):
				pass
		
		
		
def sigHandle(signum, frm): # Signal handler - Signal # and Stack Frame
	
	print "\n[!!!] Cr@wl3r is shutting down [!!!]\n"
	sleep(1)
	exit(0) #sys.exit(0)
	
	
def fileCreate():
		
	print "\n[*] Your current file directory is %s. " % os.getcwd()

	try:
		File = raw_input("[*] Please provide a name for the output file:\n\n>")
		fileOpen = open(File, "a")
		print "\n[*] Capture file %s will be written to %s." % (File, os.getcwd()) 	
		
	except:
		print "\n[*] ERROR! There was an issue creating your file. Please make sure you have write access to %s!!!!!\n" % os.getcwd	

	return fileOpen

def Jobs(Links, website, _type):

	thread = clientThread(Links, website, _type)
	thread.setDaemon(True) # Making thead a daemon thread
	thread.start() #Calls run()


def targURL():

	while True:
	
		URL = raw_input("\n[*] Please enter the website you would like to crawl. Ex. http://infosec42.blogspot.com\n\n>")
		if len(URL) != 0 and URL[0:7] == "http://" or URL[0:8] == "https://":
			break
			
		else:
			print "\n\n[!!!] Target URL cant be null and must contain http:// or https:// [!!!]\n"
			sleep(1)
			
	return str(URL)				 


def creds():
	
	while True:
		
		User = raw_input("\n[*] Please enter the username for the website using HTTP Basic Authentication:\n\n>")
		Pass = raw_input("\n[*] Please enter the password for the supplied username:\n\n>")
		if len(User) != 0:
			break
		else:
			print "\n\n[!!!] Username cant be null [!!!]\n"
			sleep(1)		
		
	return User, Pass
	
	
def basicAuth():

	global website 
	global httpRequest
	auth = None
	
	while auth != "yes" and auth != "no":
		
		auth = raw_input("\n[*] Would you like to use HTTP Basic Authentication? Please enter \"yes\" or \"no\"\n\n>")
		
		if auth == "yes":
			print "\n\n[!!!] You chose to use HTTP Basic Authentication [!!!]\n"
			sleep(.5)
			User, Pass = creds()
			basicAuth = base64.encodestring("%s:%s" % (User, Pass)).replace("\n", "")
			httpRequest.add_header("Authorization", "Basic %s" % basicAuth)
		elif auth == "no":
			print "\n\n[!!!] You chose not to use HTTP Basic Authentication. You are now continuing. [!!!]\n"
		else:
			print "\n\n[!!!] Error: You entered %s. Please enter \"yes\" or \"no\"! [!!!]\n" % auth
			
	
def main():

	global httpRequest
	signal.signal(signal.SIGINT, sigHandle) #Setting signal handler for ctrl + c
	print "\n\t--Cr@wl3r42 Web Crawler Tool--\n\n[*] Coded by Gimppy\n[*] http://infosec42.blogspot.com\n" 
	website = targURL()
	httpRequest = urllib2.Request(website)
	basicAuth()
	_file = fileCreate()
	
	try:
		html = urllib2.urlopen(httpRequest, None, 4)
		parsedHTML = BeautifulSoup(html.read(), "lxml") #lxml parser BS version 4+
		tags = ["a", "link", "script", "iframe", "img", "form", "meta", "option"]
		types = ["href", "src", "action", "content", "value"]
		Links = parsedHTML.find_all(tags)
	
		if html.code == 200:
			print "\n\n[*] %s is online. Server responded with a HTTP %d [*]\n\n" % (website, html.code)
		
		for _type in types:
			Jobs(Links, website, _type)
	
	except:
		print "\n[!!!] There was an error connecting to %s [!!!]\n" % website
		sleep(1)
		
	while True:
	
		try:	
			if work2do.empty() == True:
				break 
				
			link = work2do.get(timeout=.5)
			httpRequest = urllib2.Request(link)
			html = urllib2.urlopen(httpRequest, None, 4)
			parsedHTML = BeautifulSoup(html.read(), "lxml") #lxml parser BS version 4+
			Links = parsedHTML.find_all(tags)
						
			for _type in types:
				Jobs(Links, website, _type)
				
		except:
			print "\n[!!!] Error accessing %s . Server Response Code: %d" % (link, html.code)
		
		work2do.task_done()	
	
	work2do.join() #blocking call until work2do is empty
	print "\n[!!!] Finishing up and preparing your results. [!!!]\n"
	sleep(5)
	
	try:
		for link in allLinks:
			_file.write(link + "\n")
			
		_file.close()
	except:
		print "[!!!] Error writting results to file. [!!!]\n"		
	
	print "\n\t--RESULTS--\n[*] Total URLS processed: %d\n[*] Total unique URLS discovered: %d\n" % (new_count + discov_count, len(allLinks))			
	
if __name__ == "__main__":
	main()		
