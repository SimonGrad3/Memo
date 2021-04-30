
def izločimo_barve(barve_ki_jih_ni):
    barve = ["R", "M", "Z", "O", "V", "Y", "P"]
    if barve_ki_jih_ni != []:
            for barva in barve_ki_jih_ni:
                barve.remove(barva)
    return barve


def generator_datoteke_za_gesla (datoteka, barve_ki_jih_ni):
    barve = izločimo_barve(barve_ki_jih_ni) 

    with open (datoteka, "w") as dat:
        for barva1 in barve:
            for barva2 in barve:
                for barva3 in barve:
                    for barva4 in barve:
                        kombinacija = barva1 + barva2 + barva3 + barva4
                        dat.write(f"{kombinacija}\n")


def generator_datoteke_za_gesla_1stopnja (datoteka, barve_ki_jih_ni, pomožna="pomožna.txt"):
    generator_datoteke_za_gesla("pomožna.txt", ["V", "Y", "P"])
    with open(pomožna) as pomožna, open (datoteka, "w") as dat:
        for vrstica in pomožna:
            kombinacija = [znak for znak in vrstica.strip()]
            if len(kombinacija) == len(set(kombinacija)):
                dat.write(vrstica)
   
        


generator_datoteke_za_gesla_1stopnja("Kombinacije_level1.txt", ["V", "Y", "P"])
generator_datoteke_za_gesla("Kombinacije_level2.txt", ["Z", "O", "V", "Y", "P"])
generator_datoteke_za_gesla("Kombinacije_level3.txt", ["O", "V", "Y", "P"])
generator_datoteke_za_gesla("Kombinacije_level4.txt", ["V", "Y", "P"])
generator_datoteke_za_gesla("Kombinacije_level5.txt", ["Y", "P"])
generator_datoteke_za_gesla("Kombinacije_level6.txt", ["P"])
generator_datoteke_za_gesla("Kombinacije_level7.txt", [])

