import cloudscraper

scraper = cloudscraper.create_scraper()


def crashsite():
   games = scraper.get("https://rest-bf.blox.land/games/crash").json()
   return games

def crashpredictor():
    try:
     games = crashsite()
    except Exception as e:
      return f'Error scraping **https://rest-bf.blox.land/games/crash** \n please send this to a dev ```{e}```'
    def lol():
          r=scraper.get("https://rest-bf.blox.land/games/crash").json()["history"]
          yield [r[0]["crashPoint"], [float(crashpoint["crashPoint"]) for crashpoint in r[-2:]]]
    for game in lol():
            games = game[1]
            lastgame = game[0]
            avg = sum(games)/len(games)
            chance = 1
            for game in games:
                chance = chance = 95/game
                prediction = (1/(1-(chance))+avg)/2

                amo = {'crashchance': int(chance), 'crashprediction': int(prediction)}
                return amo

