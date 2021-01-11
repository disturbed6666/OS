#!/usr/bin/python
# -*- coding: UTF-8 -*-

BR_DRETVI = 0
broj = []
ulaz = []

def KO_init (N):
	global BR_DRETVI
	BR_DRETVI = N
	broj.extend ( [0] * N )
	ulaz.extend ( [0] * N )

def Udji_u_KO (I):
	# ostvariti prema algoritmu
	# može se koristiti funkcija max: broj[I] = max(broj) + 1
        ulaz[I] = 1
        broj[I] = max(broj) + 1
        ulaz[I] = 0

        for J in range(BR_DRETVI):
                while ulaz[J] != 0: pass
                while broj[J] != 0 and (broj[J] < broj[I] or (broj[J] == broj[I] and J < I)): pass

def Izadji_iz_KO (I):
	broj[I] = 0 # prema algoritmu
