# Naga Nannapuneni
# restaurants.py
# 11/15/21
import random
import geocoder
import requests
import json
import geopy.distance

my_api_key = "&key=YOUR_API_KEY"

g = geocoder.ip('me')
currLocCoords = (g.latlng[0], g.latlng[1])
currLocCoordsURL = str(g.latlng[0]) + "%2C" + str(g.latlng[1])

url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + currLocCoordsURL

keyword = input("What type of restaurant? (optional) ").lower().replace(" ", "%20")
if keyword != "":
    keyword = "&keyword=" + keyword
    url = url + keyword
else:
    keyword = "&keyword=food"
    url = url + keyword

maxprice = input("Maximum $s, 0 to 4? (optional) ")
if maxprice != "":
    maxprice = "&maxprice=" + maxprice
    url = url + maxprice

opennow = input("Does it have to be open now? (Y or N, optional) ").lower()
if opennow == "y":
    opennow = "&opennow=true"
    url = url + opennow
elif opennow == "n":
    opennow = "&opennow=false"
    url = url + opennow

radius = input("Maximum distance willing to go in miles? (optional) ")
if radius != "":
    radius = str(round(float(radius) * 1609.34))
    radius = "&radius=" + radius
    url = url + radius
else:
    url = url + "&radius=3200"

url = url + my_api_key
print(url, "\n")
response = requests.request("GET", url)

response = json.loads(response.text)
status = response['status']
if status == "OK":
    results = response["results"]
else:
    print(status)
    exit()


class restaurant:
    def __init__(self):
        self.name = ""
        self.businessStatus = ""
        self.openNow = ""
        self.priceLevel = ""
        self.rating = -1
        self.totalUserRatings = -1
        self.distance = -1
        self.address = ""


numPlaces = len(results)
restAttributesList = ["name", "businessStatus", "openNow", "priceLevel", "rating", "totalUserRatings", "distance", "address"]
restInstVarList = []

for i in range(numPlaces):
    currPlace = results[i]
    rest = restaurant()

    try:
        name = currPlace["name"]
        rest.name = name
    except KeyError as e:
        pass

    try:
        businessStatus = currPlace["business_status"]
        rest.businessStatus = businessStatus
    except KeyError as e:
        pass

    try:
        openNow = currPlace["opening_hours"]["open_now"]
        rest.openNow = openNow
    except KeyError as e:
        pass

    try:
        priceLevel = currPlace["price_level"]
        rest.priceLevel = priceLevel
    except KeyError as e:
        pass

    try:
        rating = currPlace["rating"]
        rest.rating = rating
    except KeyError as e:
        pass

    try:
        totalUserRatings = currPlace["user_ratings_total"]
        rest.totalUserRatings = totalUserRatings
    except KeyError as e:
        pass

    try:
        placeCoords = currPlace["geometry"]["location"]
        currPlaceCoords = (placeCoords["lat"], placeCoords["lng"])
        distance = geopy.distance.geodesic(currLocCoords, currPlaceCoords).miles
        rest.distance = distance
    except KeyError as e:
        pass

    try:
        address = currPlace["vicinity"]
        rest.address = address
    except KeyError as e:
        pass

    restInstVars = vars(rest)
    restInstVarList.append(restInstVars)

print("Total Number of Results: " + str(numPlaces))
for r in restInstVarList:
    print(r["name"] + ": ")
    for i in range(1, 8):
        a = restAttributesList[i]
        print("\t" + a + ": " + str(r[a]))
    print("\n")

print("---------------- RANDOM CHOICE --------------------")
randomChoice = random.choice(restInstVarList)
print(randomChoice["name"] + ": ")
for i in range(1, 8):
    a = restAttributesList[i]
    print("\t" + a + ": " + str(randomChoice[a]))
