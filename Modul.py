import rendom

BELA, ČRNA, NEVIDNA = "B", "Č", "N"
RDEČA, MODRA, ZELENA, ORANŽNA, VIJOLIČNA, RUMENA, ROZA = "R", "M", "Z", "O", "V","Y", "P" 

def premešaj(seznam):
    return random.shuffle(seznam)

def izloči(črka, seznam):
    return seznam.remove(črka)

class Memo:
    def __init__(self, geslo):
        self.geslo = geslo

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
    

