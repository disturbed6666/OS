brojevi = []
dupli_brojevi = []
ne_dupli_brojevi = []
uvjet = 1
while (uvjet):
	trenutniBroj = input("Unesite broj, za prekid unesite 'kraj':")
	if (trenutniBroj == "kraj"):
		uvjet = 0
		print("Unjeli ste kraj.\n")
	else:
		trenutniBroj = int(trenutniBroj)
		# print(trenutniBroj)
		for i in range (len(brojevi)):
			if (brojevi[i] == trenutniBroj):
				dupli_brojevi.append(trenutniBroj)
				break
		
		brojevi.append(trenutniBroj)

check = 0
for i in range (len(brojevi)):
	check = 0
	for j in range (len(dupli_brojevi)):
		if (brojevi[i] == dupli_brojevi[j]):
			check = 1
	if (check == 0):
		ne_dupli_brojevi.append(brojevi[i])

print(brojevi)
print(dupli_brojevi)
print(ne_dupli_brojevi)