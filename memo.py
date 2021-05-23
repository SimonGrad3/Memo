import bottle
import model

vse_igre = model.Igre()

@bottle.get("/css/<datoteka>")
def pridobi_css_datoteko(datoteka):
    return bottle.static_file(datoteka, root="css")

@bottle.get("/")
def začetna():
    return bottle.template("zacetna.html")

@bottle.post("/igra/")
def nova_igra(level=1):
    vse_igre = model.Igre.preberi_iz_datoteke(
    model.DATOTEKA_ZA_SHRANJEVANJE
    )
    id_igre = vse_igre.nova_igra(level)
    #novi_url = f"/igra/{id_igre}"

    vse_igre.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
    bottle.response.set_cookie(PIŠKOTEK_UPORABNIŠKO_IME, uporabniško_ime, path="/", secret= SKRIVNOST)
    return bottle.redirect("/igra/")

@bottle.get("/igra/")
def pokaži_igro(id_igre):
    id_igre = int(bottle.request.get_cookie(PIŠKOTEK_UPORABNIŠKO_IME, secret=SKRIVNOST))
    vse_igre = model.Igre.preberi_iz_datoteke(
    model.DATOTEKA_ZA_SHRANJEVANJE
    )

    igra, stanje = vse_igre.igre[id_igre]
    vse_igre.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
    return bottle.template("baza.html", igra=igra, id_igre=id_igre, stanje=stanje)

@bottle.post("/igra/")
def ugibaj(id_igre):
    id_igre = int(bottle.request.get_cookie(PIŠKOTEK_UPORABNIŠKO_IME, secret=SKRIVNOST))
    vse_igre = model.Igre.preberi_iz_datoteke(
    model.DATOTEKA_ZA_SHRANJEVANJE
    )
    ugib = bottle.request.forms.getunicode["ugib"]
    vse_igre.ugibaj(id_igre, ugib)
    vse_igre.zapisi_v_datoteko(model.DATOTEKA_ZA_SHRANJEVANJE)
    return bottle.redirect(f"/igra/{id_igre}")


@bottle.get("/nastavi_stopnjo/")
def nastavi_stopnjo():
    return bottle.template("nastavi_stopnjo.html")





bottle.run(reloader=True, debug=True)