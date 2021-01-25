#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function # potrebno ako se koristi Python 2
import time, threading, signal

prekini = False # zahtjev za prekid programa
otvoren = False # radnja otvorena
stolac = 0 # id klijenta kod frizerke ili 0 ako ona spava
red = [] # id-jevi klijenata koji čekaju u redu
block = 0

# definirati potrebne semafore

KO = threading.Semaphore(value=1) # inicijaliziraj semafor s poč. vr. 1
# KO je semafor koji se ovdje koristi za ostvarenje kritičnog odsječka
# početno je "zelen" (prolazan)

K1 = threading.Semaphore(value=0) # inicijaliziraj semafor s poč. vr. 0
# K1 je semafor na kojim čekaju klijenti dok ih frizerka ne pozove
# početno je "crven" (neprolazan)

K2 = threading.Semaphore(value=0) # inicijaliziraj semafor s poč. vr. 0
# K2 je semafor na koji čeka klijent kojem frizerka radi frizuru
# klijent čeka da mu se javi da je frizura gotova
# početno je "crven" (neprolazan)

K3 = threading.Semaphore(value=1) # inicijaliziraj semafor s poč. vr. 0
# sinkronizacija klijenata - da novi ne sjedne prije nego li je onaj
# s frizurom otišao

F = threading.Semaphore(value=0) # inicijaliziraj semafor s poč. vr. 0
# F je semafor na kojim čeka frizerka kad nema posla (kad "spava")
# početno je "crven" (neprolazan)

def ispisi_stanje(opis):
    global stolac, otvoren
    if otvoren: print ( "OTVORENO  ", end="" )
    else: print ( "ZATVORENO ", end="" )
    print ( "stolac: " + str(stolac), end="" )
    cekaona = red + ["-"] * (3-len(red))
    cekaona = " ".join([str(i) for i in cekaona])
    print ( " red: " + cekaona, end="" )
    print ( " [ " + opis + " ]" )

def frizerka ():
    global otvoren, prekini, stolac
    KO.acquire()# uđi u kritični odsječak
    otvoren = True # postavi oznaku OTVORENO
    ispisi_stanje("frizerka: otvaram salon")
    KO.release()# izađi iz kritičnog odsječka

    while not prekini:
        KO.acquire()# uđi u kritični odsječak
        if len(red) > 0: # ima klijenata
            K1.release()# pozovi idućeg klijenta
            KO.release()# izađi iz kritičnog odsječka
            time.sleep(5)# simuliraj rad na frizuri
            K2.release()# kraj rada na frizuri
        elif otvoren:
            stolac = 0
            ispisi_stanje("frizerka: spavam")
            KO.release()# izađi iz kritičnog odsječka
            F.acquire()# spavaj - čekaj da te probude
        else:
            stolac = 0
            ispisi_stanje("frizerka: zavrsavam s radom")
            KO.release()# izađi iz kritičnog odsječka
            break
    ispisi_stanje("frizerka: zatvaram salon i idem doma")

def klijent (id):
    global otvoren, prekini, stolac
    KO.acquire()# uđi u kritični odsječak
    if otvoren and len(red) < 3:
        red.append(id)
        ispisi_stanje("klijent " + str(id) + ": dosao")
        if stolac == 0:
            F.release() # probudi frizerku
        KO.release()# izađi iz kritičnog odsječka
        K1.acquire()# čekaj da te frizerka pozove
        K3.acquire()# čekaj da prethodni klijent ode   (NOVO)
        if prekini: return
        KO.acquire()# uđi u kritični odsječak
        stolac = id
        red.remove(id)
        ispisi_stanje("klijent " + str(id) + ": radi mi frizuru")
        KO.release()# izađi iz kritičnog odsječka
        K2.acquire()# čekaj da frizura bude gotova
        KO.acquire()# uđi u kritični odsječak
        ispisi_stanje("klijent " + str(id) + ": frizura gotova")
        K3.release()# označi da je klijent otišao   (NOVO)
    elif not otvoren:
        ispisi_stanje("klijent " + str(id) + ": salon zatvoren")
    else:
        ispisi_stanje("klijent " + str(id) + ": nema mjesta")
    KO.release()# izađi iz kritičnog odsječka

def signal_kraj ( sig_num, frame ):
    global prekini
    print ( "\nPrimljen signal za završetak ... ")
    prekini = True
    # odblokiraj frizerku i klijente ako čekaju, tj.
    # samo postavi odgovarajuće semafore da te dretve
    # mogu završiti s radom
    F.release()
    K1.release()
    K1.release()
    K1.release()
    K2.release()
    KO.release()
    K3.release()
    
def main():
    global otvoren, prekini
    signal.signal ( signal.SIGINT, signal_kraj )

    opisnik = [threading.Thread ( target = frizerka )]
    opisnik[0].start()
    for i in range(1,11):
        if prekini: break
        opisnik.append(threading.Thread ( target = klijent, args = (i,) ))
        opisnik[-1].start()
        time.sleep(2)

    KO.acquire()# uđi u kritični odsječak
    otvoren = False # postavi oznaku ZATVORENO
    ispisi_stanje("main: stavljam oznaku ZATVORENO")
    KO.release()# izađi iz kritičnog odsječka

    for i in range(11,14):
        if prekini: break
        opisnik.append(threading.Thread ( target = klijent, args = (i,) ))
        opisnik[-1].start()
        time.sleep(2)

    for i in opisnik:
        while i.is_alive():
            i.join(timeout=1)

if __name__ == "__main__":
    main()

''' Ispis izgleda ovako:
OTVORENO  stolac: 0 red: - - - [ frizerka: otvaram salon ]
OTVORENO  stolac: 0 red: - - - [ frizerka: spavam ]
OTVORENO  stolac: 0 red: 1 - - [ klijent 1: dosao ]
OTVORENO  stolac: 1 red: - - - [ klijent 1: radi mi frizuru ]
OTVORENO  stolac: 1 red: 2 - - [ klijent 2: dosao ]
OTVORENO  stolac: 1 red: 2 3 - [ klijent 3: dosao ]
OTVORENO  stolac: 1 red: 2 3 - [ klijent 1: frizura gotova ]
OTVORENO  stolac: 2 red: 3 - - [ klijent 2: radi mi frizuru ]
OTVORENO  stolac: 2 red: 3 4 - [ klijent 4: dosao ]
OTVORENO  stolac: 2 red: 3 4 5 [ klijent 5: dosao ]
OTVORENO  stolac: 2 red: 3 4 5 [ klijent 6: nema mjesta ]
OTVORENO  stolac: 2 red: 3 4 5 [ klijent 2: frizura gotova ]
OTVORENO  stolac: 3 red: 4 5 - [ klijent 3: radi mi frizuru ]
OTVORENO  stolac: 3 red: 4 5 7 [ klijent 7: dosao ]
OTVORENO  stolac: 3 red: 4 5 7 [ klijent 8: nema mjesta ]
OTVORENO  stolac: 3 red: 4 5 7 [ klijent 3: frizura gotova ]
OTVORENO  stolac: 4 red: 5 7 - [ klijent 4: radi mi frizuru ]
OTVORENO  stolac: 4 red: 5 7 9 [ klijent 9: dosao ]
OTVORENO  stolac: 4 red: 5 7 9 [ klijent 10: nema mjesta ]
ZATVORENO stolac: 4 red: 5 7 9 [ main: stavljam oznaku ZATVORENO ]
ZATVORENO stolac: 4 red: 5 7 9 [ klijent 11: salon zatvoren ]
ZATVORENO stolac: 4 red: 5 7 9 [ klijent 4: frizura gotova ]
ZATVORENO stolac: 5 red: 7 9 - [ klijent 5: radi mi frizuru ]
ZATVORENO stolac: 5 red: 7 9 - [ klijent 12: salon zatvoren ]
ZATVORENO stolac: 5 red: 7 9 - [ klijent 13: salon zatvoren ]
ZATVORENO stolac: 5 red: 7 9 - [ klijent 5: frizura gotova ]
ZATVORENO stolac: 7 red: 9 - - [ klijent 7: radi mi frizuru ]
ZATVORENO stolac: 7 red: 9 - - [ klijent 7: frizura gotova ]
ZATVORENO stolac: 9 red: - - - [ klijent 9: radi mi frizuru ]
ZATVORENO stolac: 0 red: - - - [ frizerka: zavrsavam s radom ]
ZATVORENO stolac: 0 red: - - - [ frizerka: zatvaram salon i idem doma ]
ZATVORENO stolac: 0 red: - - - [ klijent 9: frizura gotova ]
'''
