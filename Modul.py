import rendom

BELA, ČRNA, NEVIDNA = "B", "Č", "N"
RDEČA, MODRA, ZELENA, ORANŽNA, VIJOLIČNA, RUMENA, ROZA = "R", "M", "Z", "O", "V","Y", "P" 
STEVILO_POSKUSOV = 6

def premešaj(seznam):
    return random.shuffle(seznam)

def izloči(črka, seznam):
    return seznam.remove(črka)

class Memo:
    def __init__(self, geslo, level):
        self.geslo = geslo
        self.level = level

    def preveri_vrstico(self, ugibanje):
        output = []
        for i in range(4):
            if ugibanje[i] == self.geslo[i]:
                output.append(ČRNA)
                izloči(ugibanje[i], self.geslo)
            elif ugibanje[i] in self.geslo:
                output.append(BELA) 
                izloči(ugibanje[i], self.geslo)
            else:
                output.append(NEVIDNA)
        return premešaj(output)
    
    def zmaga(self, ugibanje):
        return preveri_vrstico(self, ugibanje) == [ČRNA] * 4 


def izberi_datoteko(level):
    if level == 1:
        return "Kombinacije_level1.txt"
    elif level == 2:
        return "Kombinacije_level2.txt"
    elif level == 3:
        return "Kombinacije_level3.txt"
    elif level == 4:
        return "Kombinacije_level4.txt"
    elif level == 5:
        return "Kombinacije_level5.txt"
    elif level == 6:
        return "Kombinacije_level6.txt"
    elif level == 7:
        return "Kombinacije_level7.txt"


def nova_igra(level):
    datoteka = izberi_datoteko(level)
    with open(datoteka, encoding="utf8") as dat:
        možnosti = dat.read().split()
        geslo = rendom.choice(možnosti)
    return Memo(geslo, level)
        
