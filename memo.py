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
    id_igre = vse_igre.nova_igra(level) 
    return bottle.redirect(f"/igra/{id_igre}")

@bottle.get("/igra/<id_igre:int>")
def pokaži_igro(id_igre):
    igra, stanje = vse_igre.igre[id_igre]
    return bottle.template("baza.html", igra=igra, id_igre=id_igre, stanje=stanje)

@bottle.post("/igra/<id_igre:int>")
def ugibaj(id_igre):
    ugib = bottle.request.forms.getunicode("ugib")
    vse_igre.ugibaj(id_igre, ugib)
    return bottle.redirect(f"/igra/{id_igre}")


@bottle.get("/nastavi_stopnjo/")
def nastavi_stopnjo():
    return bottle.template("nastavi_stopnjo.html")





bottle.run(reloader=True, debug=True)