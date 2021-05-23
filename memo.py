import bottle
import model

PIŠKOTEK_UPORABNIŠKO_IME = "prijavljen"
SKRIVNOST = "ofnweo93km'1md'md"



@bottle.get("/css/<datoteka>")
def pridobi_css_datoteko(datoteka):
    return bottle.static_file(datoteka, root="css")



def shrani_stanje(uporabnik):
    uporabnik.v_datoteko()

def trenutni_uporabnik():
    uporabniško_ime = bottle.request.get_cookie(PIŠKOTEK_UPORABNIŠKO_IME, secret= SKRIVNOST)
    if uporabniško_ime:
        try:
            vse_igre = model.Uporabnik.iz_datoteke(uporabniško_ime)
        except FileNotFoundError:
            bottle.redirect("/registracija/")
    else:
        bottle.redirect("/prijava/")
    return uporabniško_ime

@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napaka=None)

@bottle.post("/prijava/")
def prijava_post():
    uporabniško_ime = bottle.request.forms.getunicode("uporaniško_ime")
    geslo = bottle.request.forms.getunicode("geslo")
    if geslo == "geslo":
        bottle.response.set_cookie(PIŠKOTEK_UPORABNIŠKO_IME, uporabniško_ime, path="/", secret= SKRIVNOST)
        bottle.redirect("/")
    else:
        return bottle.template("prijava.html", napaka="Geslo je napačno!")
            
@bottle.get("/registacija/")
def registracija_get():
    return bottle.template("registracija.html", napaka=None)

@bottle.post("/registacija/")
def registracija_post():
    uporabniško_ime = bottle.request.forms.getunicode("uporaniško_ime")
    geslo = bottle.request.forms.getunicode("geslo")
    model.Uporabnik(uporabniško_ime, model.Igre())
    bottle.redirect("/")


@bottle.get("/")
def začetna():
    uporabnik = trenutni_uporabnik()
    return bottle.template("zacetna.html", uporabnik=uporabnik)

@bottle.post("/igra/")
def nova_igra(level=1):
    uporabnik = trenutni_uporabnik()
    id_igre = uporabnik.vse_igre.nova_igra(level)
    #novi_url = f"/igra/{id_igre}"

    shrani_stanje(uporabnik)
    bottle.response.set_cookie(PIŠKOTEK_UPORABNIŠKO_IME, uporabnik, path="/", secret= SKRIVNOST)
    return bottle.redirect("/igra/")

@bottle.get("/igra/")
def pokaži_igro(id_igre):
    id_igre = int(bottle.request.get_cookie(PIŠKOTEK_UPORABNIŠKO_IME, secret=SKRIVNOST))
    uporabnik = trenutni_uporabnik()

    igra, stanje = uporabnik.vse_igre.igre[id_igre]
    shrani_stanje(uporabnik)
    return bottle.template("baza.html", igra=igra, id_igre=id_igre, stanje=stanje)

@bottle.post("/igra/")
def ugibaj(id_igre):
    id_igre = int(bottle.request.get_cookie(PIŠKOTEK_UPORABNIŠKO_IME, secret=SKRIVNOST))
    uporabnik = trenutni_uporabnik()
    ugib = bottle.request.forms.getunicode["ugib"]

    uporabnik.vse_igre.ugibaj(id_igre, ugib)
    shrani_stanje(uporabnik)
    return bottle.redirect(f"/igra/{id_igre}")


@bottle.get("/nastavi_stopnjo/")
def nastavi_stopnjo():
    return bottle.template("nastavi_stopnjo.html")





bottle.run(reloader=True, debug=True)