import bottle
import model
from datetime import date

PISKOTEK_UPORABNISKO_IME = "prijavljen"
SKRIVNOST = "ofnweo93km'1md'md"



@bottle.get("/css/<datoteka>")
def pridobi_css_datoteko(datoteka):
    return bottle.static_file(datoteka, root="css")


def nastavi_piškotek(uporabnisko_ime, id_igre):
    bottle.response.set_cookie(
        PISKOTEK_UPORABNISKO_IME, uporabnisko_ime+ "-" + str(id_igre), path="/", secret=SKRIVNOST
        )

def shrani_stanje(uporabnik):
    uporabnik.v_datoteko()

def pridobi_iz_niza(niz):
    if niz == None:
        bottle.redirect("/prijava/")
    else:
        ime, id = niz.split("-")
        return ime, int(id)

def trenutni_id():
    piškotek= bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST
        )
    _, id = pridobi_iz_niza(piškotek)
    return id

def trenutni_uporabnik():
    piškotek = bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST
        )
    ime, _ = pridobi_iz_niza(piškotek)
    if ime:
        return podatki_uporabnika(ime)
    else:
        bottle.redirect("/prijava/")

def podatki_uporabnika(uporabniško_ime):
    try:
        return model.Uporabnik.iz_datoteke(uporabniško_ime)
    except FileNotFoundError:
        bottle.redirect("/registracija/")

@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napaka=None)

@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    napisano_geslo = bottle.request.forms.getunicode("geslo")
    if uporabnisko_ime: 
        uporabnik = podatki_uporabnika(uporabnisko_ime)
        if uporabnik.preveri_geslo(napisano_geslo):
            nastavi_piškotek(uporabnisko_ime, 0)
            bottle.redirect("/")
        else:
            return bottle.template("prijava.html", napaka="Geslo je napačno!")
    else: 
        return bottle.template("prijava.html", napaka="Nisi vpisal uporabniškega imena!")
            
@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napaka=None)

@bottle.post("/registracija/")
def registracija_post():
    uporabniško_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    napisano_geslo = bottle.request.forms.getunicode("geslo")

    try: 
        model.Uporabnik.iz_datoteke(uporabniško_ime) #zgolj za to, da vrne napako
        return bottle.template("registracija.html", napaka="To uporabniško ime že obstaja!")
    except FileNotFoundError:    
        naredi_novega_uporabnika(uporabniško_ime, napisano_geslo)

def naredi_novega_uporabnika(uporabniško_ime, napisano_geslo):
    novi_uporabnik = model.Uporabnik(
            uporabniško_ime, model.zašifriraj_geslo(napisano_geslo), model.Igre()
            )
    nastavi_piškotek(uporabniško_ime, 0)
    novi_uporabnik.v_datoteko()
    bottle.redirect("/")

@bottle.post("/odjava/")
def odjava_post():
    bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME ,path="/")
    bottle.redirect("/")


@bottle.get("/")
def začetna():
    uporabnik = trenutni_uporabnik()
    return bottle.template("zacetna.html", uporabnik=uporabnik)

@bottle.get("/igra/<level>")
def nova_igra(level=1):
    uporabnik = trenutni_uporabnik()
    id_igre = uporabnik.igre.nova_igra(level)
    shrani_stanje(uporabnik)
    nastavi_piškotek(uporabnik.uporabniško_ime, id_igre)
    return bottle.redirect("/igraj/")

@bottle.get("/igraj/")
def pokaži_igro():
    uporabnik = trenutni_uporabnik()
    id_igre = trenutni_id()

    igra, stanje = uporabnik.igre.igre[id_igre]
    napake = igra.št_napak()
    shrani_stanje(uporabnik)
    return bottle.template("baza.html", igra=igra, id_igre=id_igre, stanje=stanje, napake=napake)

@bottle.post("/igraj/")
def ugibaj():
    uporabnik = trenutni_uporabnik()
    id_igre = trenutni_id()
    ugib = bottle.request.forms.getunicode("ugib")
    igra, _ = uporabnik.igre.igre[id_igre]

    if igra.preveri_vstavitev(ugib):
        uporabnik.igre.ugibaj(id_igre, ugib)
        shrani_stanje(uporabnik)
        return bottle.redirect("/igraj/")
    else:
        return bottle.redirect("/igraj/")


@bottle.get("/nastavi_stopnjo/")
def nastavi_stopnjo_get():
    return bottle.template("nastavi_stopnjo.html")

@bottle.post("/nastavi_stopnjo/")
def nastavi_stopnjo_post():
    level = bottle.request.forms.getunicode("level")
    bottle.redirect(f"/igra/{level}")

@bottle.post("/mojster/")
def mojster():
    mojster = bottle.request.forms.getunicode("mojster")
    datum = date.today().strftime("%Y/%m/%d")
    model.v_mojstre(mojster, datum)
    return bottle.redirect("/")

@bottle.get("/mojstri/")
def pokaži_mojster():
    seznam_vseh_mojstrov = model.iz_mojstrov()
    return bottle.template("mojstri.html", seznam_vseh_mojstrov=seznam_vseh_mojstrov)

@bottle.get("/navodila/")
def pokaži_igre():
    return bottle.template("navodila.html")



bottle.run(reloader=True, debug=True)