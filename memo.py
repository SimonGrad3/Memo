import bottle
import model

PISKOTEK_UPORABNISKO_IME = "prijavljen"
SKRIVNOST = "ofnweo93km'1md'md"



@bottle.get("/css/<datoteka>")
def pridobi_css_datoteko(datoteka):
    return bottle.static_file(datoteka, root="css")



def shrani_stanje(uporabnik):
    uporabnik.v_datoteko()

def trenutni_uporabnik():
    uporabniško_ime = bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret= SKRIVNOST
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
    print(bottle.request.forms)
    napisano_geslo = bottle.request.forms.getunicode("geslo")
    if uporabnisko_ime:
        uporabnik = podatki_uporabnika(uporabnisko_ime)
        if uporabnik.preveri_geslo(napisano_geslo):
            bottle.response.set_cookie(
                PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret= SKRIVNOST
                )
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

    if uporabniško_ime:
        return bottle.template("registracija.html", napaka="To uporabniško ime že obstaja!")
    else:    
        novi_uporabnik = model.Uporabnik(
            uporabniško_ime, model.zašifriraj_geslo(napisano_geslo), model.Igre()
            )
        novi_uporabnik.v_datoteko()
        bottle.redirect("/")


@bottle.get("/")
def začetna():
    uporabnik = trenutni_uporabnik()
    return bottle.template("zacetna.html", uporabnik=uporabnik)

@bottle.post("/igra/")
def nova_igra(level=1):
    uporabnik = trenutni_uporabnik()
    id_igre = uporabnik.vse_igre.nova_igra(level)
    novi_url = f"/igra/{id_igre}"
    shrani_stanje(uporabnik)
    bottle.response.set_cookie(
        PISKOTEK_UPORABNISKO_IME, uporabnik, path="/", secret= SKRIVNOST
        )
    return bottle.redirect("/igra/")

@bottle.get("/igra/")
def pokaži_igro(id_igre):
    id_igre = int(bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST
        ))
    uporabnik = trenutni_uporabnik()

    igra, stanje = uporabnik.vse_igre.igre[id_igre]
    shrani_stanje(uporabnik)
    return bottle.template("baza.html", igra=igra, id_igre=id_igre, stanje=stanje)

@bottle.post("/igra/")
def ugibaj(id_igre):
    id_igre = int(bottle.request.get_cookie(
        PISKOTEK_UPORABNISKO_IME, secret=SKRIVNOST
        ))
    uporabnik = trenutni_uporabnik()
    ugib = bottle.request.forms.getunicode["ugib"]

    uporabnik.vse_igre.ugibaj(id_igre, ugib)
    shrani_stanje(uporabnik)
    return bottle.redirect(f"/igra/{id_igre}")


@bottle.get("/nastavi_stopnjo/")
def nastavi_stopnjo():
    return bottle.template("nastavi_stopnjo.html")





bottle.run(reloader=True, debug=True)