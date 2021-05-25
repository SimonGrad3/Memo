import bottle
import model

PISKOTEK_UPORABNISKO_IME = "prijavljen"
SKRIVNOST = "ofnweo93km'1md'md"



@bottle.get("/css/<datoteka>")
def pridobi_css_datoteko(datoteka):
    return bottle.static_file(datoteka, root="css")


def nastavi_piškotek(uporabnisko_ime, id_igre):
    bottle.response.set_cookie(
        PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, id_igre, path="/", secret=SKRIVNOST
        )

def shrani_stanje(uporabnik):
    uporabnik.v_datoteko()

def trenutni_id():
    piškotek_id_igre = bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST
        )

    if piškotek_id_igre:
        return int(piškotek_id_igre)
    else:
        bottle.redirect("/igra/")

def trenutni_uporabnik():
    uporabniško_ime = bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST
        )
    if uporabniško_ime:
        return podatki_uporabnika(uporabniško_ime)
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


@bottle.get("/")
def začetna():
    uporabnik = trenutni_uporabnik()
    return bottle.template("zacetna.html", uporabnik=uporabnik)

@bottle.post("/igra/<level>")
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
    shrani_stanje(uporabnik)
    return bottle.template("baza.html", igra=igra, id_igre=id_igre, stanje=stanje)

@bottle.post("/igraj/")
def ugibaj():
    uporabnik = trenutni_uporabnik()
    id_igre = trenutni_id()
    ugib = bottle.request.forms.getunicode["ugib"]

    uporabnik.igre.ugibaj(id_igre, ugib)
    shrani_stanje(uporabnik)
    return bottle.redirect(f"/igra/{id_igre}")


@bottle.get("/nastavi_stopnjo/")
def nastavi_stopnjo():
    return bottle.template("nastavi_stopnjo.html")

@bottle.post("/nastavi_stopnjo/")
def nastavi_stopnjo():
    level = bottle.request.forms.getunicode("uporabnisko_ime")
    bottle.redirect(f"/igra/{level}")





bottle.run(reloader=True, debug=True)