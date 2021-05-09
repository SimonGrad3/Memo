import random

BELA, ČRNA, NEVIDNA = "B", "Č", "N"
RDEČA, MODRA, ZELENA, ORANŽNA, VIJOLIČNA, RUMENA, ROZA = "R", "M", "Z", "O", "V", "Y", "P" 
STEVILO_POSKUSOV = 6

def premešaj(seznam):
    return random.shuffle(seznam)

def izloči(črka, seznam):
    """Iz seznama izloči črko"""
    return seznam.remove(črka)

class Memo:
    def __init__(self, geslo, level, ugibanja=None):
        self.geslo = geslo
        self.level = level
        self.ugibanja = ugibanja or list()
    
    def __repr__(self):
        return f"Memo({self.geslo}, {self.level}, {self.ugibanja})"

    def preveri_vrstico(self, ugibanje):
        self.ugibanja.append(ugibanje)
        output = list()
        geslo_za_preverjanje = [i for i in self.geslo]
        ugibanje_za_preverjanje = [i for i in ugibanje]
        
        """Preveri za tiste, ki so na iste barve na istem mestu"""
        for i in range(4):
            if ugibanje_za_preverjanje[3-i] == geslo_za_preverjanje[3-i]:
                output.append(ČRNA)
                geslo_za_preverjanje.pop(3-i)
                ugibanje_za_preverjanje.pop(3-i)

        """Preveri še ostale"""
        n = len(ugibanje_za_preverjanje)
        for i in range(n):
            if ugibanje_za_preverjanje[n-i-1] in geslo_za_preverjanje:
                output.append(BELA)
                izloči(ugibanje_za_preverjanje[n-i-1], geslo_za_preverjanje)
            else:
                output.append(NEVIDNA)

        return output

    def št_napak(self):
        return len(self.ugibanja)

    def zmaga(self, ugibanje):
        return preveri_vrstico(self, ugibanje) == [ČRNA] * 4 


def izberi_datoteko(level):
    return f"Kombinacije_level{level}.txt"

def nova_igra(level):
    datoteka = izberi_datoteko(level)
    with open(datoteka, encoding="utf8") as dat:
        možnosti = dat.read().split()
        geslo_str = random.choice(možnosti)
        geslo = [barva for barva in geslo_str]
    return Memo(geslo, level)
        
