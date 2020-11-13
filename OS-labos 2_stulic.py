#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time, signal, sys

TEKUCI_PRIORITET = 0
PRIORITET = [0,0,0,0,0,0]
OZNAKA_CEKANJA = [0,0,0,0,0,0]

def ispisi_pojavu_signala ( prioritet ): # prioritet u rangu 1-5
	print ( '\t' + '- ' * prioritet + 'X ' + '- ' * (5-prioritet) )
def ispisi_pocetak_obrade_signala ( prioritet ):
	print ( '\t' + '- ' * prioritet + 'P ' + '- ' * (5-prioritet) )
def ispisi_kraj_obrade_signala ( prioritet ):
	print ( '\t' + '- ' * prioritet + 'K ' + '- ' * (5-prioritet) )
def ispisi_korak_obrade_signala ( prioritet, korak ):
	print ( '\t' + '- ' * prioritet + str(korak) + ' ' + '- ' * (5-prioritet) )
def ispisi_korak_obrade_glavnog_programa ( korak ):
	print ( '\t' + str(korak%10) + ' -' * 5 )

def simulacija_obrade_prekida ( prioritet ):
	ispisi_pocetak_obrade_signala ( prioritet )
	for korak in range(1,6):
		ispisi_korak_obrade_signala ( prioritet, korak )
		time.sleep(1)
	ispisi_kraj_obrade_signala ( prioritet )

def prekidna_rutina ( signal, frame ):
	global TEKUCI_PRIORITET
	global PRIORITET
	global OZNAKA_CEKANJA
	prioritet = int(input("Unesi prioritet prekida: "))
	if prioritet == 10:
		print ( "\nZavršavam rad" )
		sys.exit(1)

	ispisi_pojavu_signala ( prioritet )
	OZNAKA_CEKANJA[prioritet] += 1

	# ostatak koda prema predlošku
	# ...
	while prioritet > TEKUCI_PRIORITET :
		OZNAKA_CEKANJA[prioritet] -= 1 
		PRIORITET[prioritet] = TEKUCI_PRIORITET
		TEKUCI_PRIORITET = prioritet
		simulacija_obrade_prekida ( prioritet )
		TEKUCI_PRIORITET = PRIORITET[prioritet]
		prioritet = 0
		for i in range (TEKUCI_PRIORITET+1, 6):
			if OZNAKA_CEKANJA[i] != 0:
				prioritet = i
	# ...

def main():
	print("CTRL+C ZA UNOS SIGNALA; A PRIORITET 10 ZA ZAVRŠETAK PROGRAMA\n\n")
	print("\tG 1 2 3 4 5")

	signal.signal ( signal.SIGINT, prekidna_rutina )

	for korak in range(100):
		ispisi_korak_obrade_glavnog_programa ( korak )
		time.sleep(1)

if __name__ == "__main__":
	main()
