import random
import json

BELA, ČRNA, NEVIDNA = "B", "Č", "N"
RDEČA, MODRA, ZELENA, ORANŽNA, VIJOLIČNA, RUMENA, ROZA = "R", "M", "Z", "O", "V", "Y", "P" 
ZMAGA, PORAZ = "ČČČČ", "L"
ZAČETEK = "S"
ŠTEVILO_POSKUSOV = 6



def premešaj(seznam):
    return random.shuffle(seznam)

def izloči(črka, seznam):
    """Iz seznama izloči črko"""
    return seznam.remove(črka)

class Memo:
    def __init__(self, level, geslo, ugibanja=None):
        self.geslo = geslo
        self.level = level
        self.ugibanja = ugibanja or list()
    
    def __repr__(self):
        return f"Memo({self.level}, {self.geslo}, {self.ugibanja})"

    def preveri_vrstico(self, ugibanje):
        output = list()
        geslo_za_preverjanje = [i for i in self.geslo]
        ugibanje_za_preverjanje = [i for i in ugibanje]
        
        """Preveri (ČRNE), če je kakšna ista barva na istem mestu"""
        for i in range(4):
            if ugibanje_za_preverjanje[3-i] == geslo_za_preverjanje[3-i]:
                output.append(ČRNA)
                geslo_za_preverjanje.pop(3-i)
                ugibanje_za_preverjanje.pop(3-i)

        """Preveri še ostale (BELE, NEVIDNE)"""
        n = len(ugibanje_za_preverjanje)
        for i in range(n):
            if ugibanje_za_preverjanje[n-i-1] in geslo_za_preverjanje:
                output.append(BELA)
                izloči(ugibanje_za_preverjanje[n-i-1], geslo_za_preverjanje)
            else:
                output.append(NEVIDNA)

        premešaj(output)
        return output

    def št_napak(self):
        return len(self.ugibanja)

    def zmaga(self, ugibanje):
        return self.preveri_vrstico(ugibanje) == [ČRNA] * 4 

    def poraz(self):
        return self.št_napak() > ŠTEVILO_POSKUSOV

    def igraj(self, ugibanje):
        self.ugibanja.append(ugibanje)

        if self.zmaga(ugibanje):
            return ZMAGA
        elif self.poraz():
            return PORAZ
        else:
            return(self.preveri_vrstico(ugibanje))

    def pretvori_v_json_slovar(self):
        return{
            "level": self.level,
            "geslo": self.geslo,
            "ugibanja" : self.ugibanja,            
        }

    @staticmethod
    def dobi_iz_json_slovarja(slovar):
        return Memo(slovar["level"], slovar["geslo"], slovar["ugibanja"])



def izberi_datoteko(level):
    return f"Kombinacije_level{level}.txt"

def nova_igra(level):
    datoteka = izberi_datoteko(level)
    with open(datoteka, encoding="utf8") as dat:
        možnosti = dat.read().split()
        geslo_str = random.choice(možnosti)
        geslo = [barva for barva in geslo_str]
    return Memo( level ,geslo)





class Igre:
    def __init__(self, začetne_igre=None, začetni_id=0):
        self.igre = začetne_igre or {}
        self.max_id = začetni_id

    def pretvori_v_json_slovar(self):
        slovar_iger= {}

        for id_igre, (igra, stanje) in self.igre.items():
            slovar_iger[id_igre] = (
                igra.pretvori_v_json_slovar(),
                stanje
            )
        
        return {
            "max_id": self.max_id,
            "igre": slovar_iger
        }

    def zapisi_v_datoteko(self, datoteka):
        with open(datoteka, "w") as dat:
            json_slovar = self.pretvori_v_json_slovar()
            json.dump(json_slovar, dat, indent=3)

    def dobi_iz_json_slovarja(slovar):
        slovar_iger = {}
        for id_igre, (igra_slovar, stanje) in slovar["igre"].items():
            slovar_iger[int(id_igre)] = (
                Memo.dobi_iz_json_slovarja(igra_slovar), stanje
            )
        
        return Igre(slovar_iger, slovar["max_id"])

    @staticmethod
    def preberi_iz_datoteke(datoteka):
        with open(datoteka, "r") as in_file:
            json_slovar = json.load(in_file)
        return Igre.dobi_iz_json_slovarja(json_slovar)



    def prost_id_igre(self):
        self.max_id += 1
        return self.max_id

    def nova_igra(self, level):
        """Sestavi novo igro z naključnim geslom"""
        nov_id = self.prost_id_igre()
        trenutna_igra = nova_igra(level)

        self.igre[nov_id] = (trenutna_igra, ZAČETEK)
        return nov_id

    def ugibaj(self, id_igre, ugib):
        """Ob ugibanju vrne rezultat ter spremeni stanje"""
        igra, _ = self.igre[id_igre]
        novo_stanje = igra.igraj(ugib)
        self.igre[id_igre] = (igra, novo_stanje)



def zašifriraj_geslo(geslo):
    zašifrirano_geslo = ""
    for črka in geslo:
        zašifrirano_geslo += črka + "pa"
    return zašifrirano_geslo


class Uporabnik:
    def __init__(self, uporabniško_ime, zašifrirano_geslo, igre):
        self.uporabniško_ime = uporabniško_ime
        self.zašifrirano_geslo = zašifrirano_geslo
        self.igre = igre
    
    def v_slovar(self):
        return {
            "uporabnisko_ime": self.uporabniško_ime,
            "zasifrirano_geslo": self.zašifrirano_geslo,
            "igre": self.igre.pretvori_v_json_slovar()
        }

    def v_datoteko(self):
        with open(Uporabnik.ime_uporabnikove_datoteke(self.uporabniško_ime), "w", encoding="UTF-8") as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=5)

    @staticmethod
    def ime_uporabnikove_datoteke(uporabniško_ime):
        return f"{uporabniško_ime}.json"

    @staticmethod
    def iz_slovarja(slovar):
        uporabniško_ime = slovar["uporabnisko_ime"]
        geslo = slovar["zasifrirano_geslo"]
        igre = Igre.dobi_iz_json_slovarja(slovar["igre"])
        return Uporabnik(uporabniško_ime, geslo, igre)

    @staticmethod
    def iz_datoteke(uporabniško_ime):
        with open(Uporabnik.ime_uporabnikove_datoteke(uporabniško_ime), encoding="UTF-8") as dat:
            slovar = json.load(dat)
            return Uporabnik.iz_slovarja(slovar)

    def nastavi_geslo(self, napisano_geslo):
        self.zašifrirano_geslo = zašifriraj_geslo(napisano_geslo)

    def preveri_geslo(self, napisano_geslo):
        return self.zašifrirano_geslo == zašifriraj_geslo(napisano_geslo)
