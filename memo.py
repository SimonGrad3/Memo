import bottle
import model

@bottle.get("/css/<datoteka>")
def pridobi_css_datoteko(datoteka):
    return bottle.static_file(datoteka, root="css")

@bottle.get("/")
def začetna():
    return bottle.template("zacetna.html")

@bottle.get("/igra/")
def pokaži_igro():
    return bottle.template("baza.html")

@bottle.get("/nastavi_stopnjo/")
def nastavi_stopnjo():
    return bottle.template("nastavi_stopnjo.html")





bottle.run(reloader=True, debug=True)