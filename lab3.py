#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time, threading, signal, sys, random
from lamport import KO_init, Udji_u_KO, Izadji_iz_KO

kraj = False     # na signal ova se varijabla mijenja

# broj dretvi i stolova se zadaje preko komandne linije
BR_DRETVI = -1
BR_STOLOVA = -1

stol = []
slobodno = 0 # broj slobodnih stolova

def odaberi_slobodni_stol():
    '''
    Funkcija vraća indeks nasumično odabranog slobodnog stola
    ili -1 ako nema slobodnog stola.
    Ovo se može napraviti na razne načine. Jedan je opisan u nastavku.
    '''
    # dok je slobodno > 0 radi
    #   x = slučajan broj od 0 do slobodno-1
    #   y = 0
    #   za i = 0 do BR_STOLOVA-1 radi
    #       ako je stol[i] == 0 tada
    #           ako je x == y tada
    #               vrati i
    #           inače
    #               y = y + 1
    while slobodno > 0:
        x = random.randint(0, slobodno-1)
        y = 0
        for i in range(BR_STOLOVA):
            if stol[i] == 0:
                if x == y:
                    return i
                else:
                    y += 1
    
    return -1 # nema slobodnih stolova

def ispisi_stanje ():
    stanje = "".join ( str(x) if x > 0 else "-" for x in stol )
    print ( "Stolovi: " + stanje )

def posao_dretve (id):
    ''' Početna funkcija za nove dretve '''
    global slobodno
    while not kraj: # dok signal za kraj nije došao
        i = odaberi_slobodni_stol ()
        if i == -1:
            break
        print ( "Dretva " + str(id) + ": odabirem stol " + str(i) )
        time.sleep(1.0)

        Udji_u_KO (id-1) # id ide od 1-N, a polja od 0 do N-1
        if stol[i] == 0:
            stol[i] = id
            slobodno = slobodno - 1
            print ( "Dretva " + str(id) + ": rezerviram stol " + str(i) )
        else:
            print ( "Dretva " + str(id) + ": neuspjela rezervacija stola " + str(i) )
        ispisi_stanje ()
        Izadji_iz_KO (id-1)

        time.sleep(1.0)

def signal_kraj ( sig_num, frame ):
    ''' Na signal SIGINT (Ctrl+C) program završava '''
    print ( "\nPrimljen signal za završetak ... ")
    global kraj
    kraj = True

def main():
    signal.signal ( signal.SIGINT, signal_kraj )

    global BR_DRETVI, BR_STOLOVA, slobodno
    if len(sys.argv) == 3:
        BR_DRETVI = int(sys.argv[1])
        BR_STOLOVA = int(sys.argv[2])
        slobodno = BR_STOLOVA
    else:
        print ( "Korištenje: python lab3 ")
        sys.exit(1)

    KO_init (BR_DRETVI)
    stol.extend ( [0] * BR_STOLOVA ) # u početku su svi stolovi slobodni
    ispisi_stanje ()
    dretva = [None] * BR_DRETVI
    for i in range(BR_DRETVI):
        dretva[i] = threading.Thread ( target = posao_dretve, args = (i+1,) )
        dretva[i].start()

    for i in range(BR_DRETVI):
        while dretva[i].is_alive():
            dretva[i].join (timeout=1)

    if not kraj:
        print ( "Svi stolovi zauzeti" )

if __name__ == "__main__":
    main()
