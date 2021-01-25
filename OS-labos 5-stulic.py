#!/usr/bin/python
# -*- coding: UTF-8 -*-

# simulacija rasproređivanja SCHED_RR
import time

''' Primjer osnovna korištenja klasa u Pythonu '''
class Dretva:
    def __init__ ( self, trenutak_pojave, broj, prioritet, trajanje ):
        self.t = trenutak_pojave  # kada se dretva pojavljuje
        self.id = broj            # identifikacijski broj dretve
        self.c = trajanje         # koliko još vremena treba
        self.p = prioritet        # prioritet dretve

    def ispisi ( self ):
        print ( self.id, self.p, self.c, "\t", end="" )

class Aktivna_D:
    def __init__ ( self ):
        self.dretva = None
        
    def dohvati ( self ):
        return self.dretva

    def postavi ( self, dretva ):
        self.dretva = dretva

    def odradila_kvant ( self ):
        if self.dretva:
            self.dretva.c -= 1
            if self.dretva.c == 0:
                print ( "Zavrsila dretva " + str(self.dretva.id))
                self.dretva = None

    def ispisi ( self ):
        if self.dretva:
            self.dretva.ispisi()

class Pripravne_D:
    def __init__ ( self, broj_prioriteta ):
        self.n = broj_prioriteta + 1
        self.red = [[] for i in range(self.n)]

    def dodaj ( self, dretva ):
        if dretva:
            self.red[dretva.p].append ( dretva )

    def uzmi_prvu ( self ):
        for i in range ( self.n-1, -1, -1 ): # od broja prioriteta do 0
            if self.red[i]:
                dretva = self.red[i].pop(0)
                return dretva
        return None

    def ispisi ( self ):
        for i in range ( self.n-1, -1, -1 ): # od broja prioriteta do 0
            for dretva in self.red[i]:
                dretva.ispisi()

class Rasporedjivac:
    def __init__ ( self, aktivna, pripravne ):
        self.aktivna = aktivna
        self.pripravne = pripravne
        self.t = 0 # vrijeme

    def sched_fifo_korak ( self ):
        self.aktivna.odradila_kvant()
        if not self.aktivna.dohvati(): # Ako je aktivna gotova vratit će FALSE što not daje TRUE
            self.aktivna.postavi ( self.pripravne.uzmi_prvu() )
        self.t += 1

    def sched_rr_korak ( self ):
        # napraviti:
        self.aktivna.odradila_kvant() # 1. aktivna je odradila kvant
        self.pripravne.dodaj(self.aktivna.dretva) # 2. makni aktivnu u pripravne
        self.aktivna.postavi(self.pripravne.uzmi_prvu()) # 3. uzmi prvu pripravnu i učini ju aktivnom
        self.t += 1

    def sched_dodaj ( self, dretva ):
        # napraviti:
        if not self.aktivna.dohvati(): # ako nema aktivne dretve tada
            self.aktivna.postavi(dretva) # postavi "dretva" kao aktivnu
        else: # inače
            if dretva.p > self.aktivna.dretva.p: # ako je "dretva" većeg prioriteta od aktivne tada
                self.pripravne.dodaj(self.aktivna.dretva) # spremi aktivnu u red pripravnih
                self.aktivna.postavi(dretva) # postavi "dretva" kao aktivnu
            else: # inače
                self.pripravne.dodaj(dretva) # spremi "dretva" u red pripravnih

        self.ispisi ( "Dodana dretva " + str(dretva.id) )

    def ispisi ( self, msg="" ):
        print ( self.t, "\t", end="" )
        self.aktivna.ispisi()
        self.pripravne.ispisi()
        print(msg)

def main():
    dretve = []           # t   id prio trajanje
    dretve.append ( Dretva (1,  51, 5,   10) )
    dretve.append ( Dretva (3,  52, 5,   7) )
    dretve.append ( Dretva (7,  31, 3,   5) )
    dretve.append ( Dretva (12, 53, 5,   3) )
    dretve.append ( Dretva (22, 32, 3,   6) )
    dretve.append ( Dretva (30, 41, 4,   3) )

    max_prio = max ( [x.p for x in dretve] )
    rasporedjivac = Rasporedjivac ( Aktivna_D(), Pripravne_D(max_prio) )

    print ( "t\tAktivna\tPripravne")
    while dretve or rasporedjivac.aktivna.dohvati():
        rasporedjivac.ispisi()
        rasporedjivac.sched_rr_korak() # zamijeniti sa: sched_rr_korak
        while dretve and dretve[0].t == rasporedjivac.t:
            rasporedjivac.sched_dodaj ( dretve.pop(0) )
        time.sleep(1)

if __name__ == "__main__":
    main()
