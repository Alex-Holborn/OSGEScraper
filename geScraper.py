import urllib.request
import time
import json

class GeScraper:

    def __init__(self):
        self.data = []
        self.base_url = "http://services.runescape.com/m=itemdb_oldschool/api/catalogue/detail.json?item="

    def loopItemIDs(self):
        for i in range(0, 1093):
            for j in range(0, 20):
                self.tryScrapeID((i*20) + j)
        self.save_json_file()

    def tryScrapeID(self, id):
        response = self.getUrlResponse("{}{}".format(self.base_url, id))
        if response == "404":
            pass
        elif response.info()["Content-Length"] == "0":
            time.sleep(60)
            self.tryScrapeID(id)
        else:
            j = json.load(response)
            self.displayInterestingInfo(j)


    def getUrlResponse(self, url):
        try:
            return urllib.request.urlopen(url, timeout=10)
        except urllib.request.HTTPError as e:
            return "404"

    def displayInterestingInfo(self, j):
        print(
            "{} | description: {} | current price: {} | 30 day change: {} | 90 day change: {} | 180 day change: {}".format(
                j["item"]["name"], j["item"]["description"], j["item"]["current"]["price"],
                j["item"]["day30"]["change"], j["item"]["day90"]["change"], j["item"]["day180"]["change"]))

    def add_data(self, json_data):
        self.data.append(json_data)

    def save_json_file(self):
        with open("json_data.txt", "w") as out_file:
            json.dump(self.data, out_file)


g = GeScraper()
g.loopItemIDs()
