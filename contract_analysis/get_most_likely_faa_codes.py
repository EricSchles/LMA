from uszipcode import ZipcodeSearchEngine
import pandas as pd
from geopy.distance import vincenty
import code
import itertools

df = pd.read_csv("TAGGS Export 4rawnez1.ic4.csv")

df["index"] = range(len(df))
df["ZIP Code"] = df["ZIP Code"].astype(str)
contract_zipcode = []
for contract_idx in df.index:
    search = ZipcodeSearchEngine()
    zipcode = search.by_zipcode(
        df.loc[contract_idx]["ZIP Code"][:5]
    )
    contract_lat_long = (zipcode["Latitude"], zipcode["Longitude"])
    contract_identifier = df.loc[contract_idx]["index"]
    if contract_lat_long[0] is None:
        continue
    contract_zipcode.append((contract_identifier, contract_lat_long))

airports = pd.read_csv("airport_codes.csv")
airports = airports[(airports["type"] == "small_airport")
                    | (airports["type"] == "medium_airport")
                    | (airports["type"] == "large_airport")]
airports = airports[airports["iso_country"] == "US"]
airports = airports[pd.notnull(airports["iata_code"])]

airport_zipcode = []
for idx in airports.index:
    coordinates = airports.loc[idx]["coordinates"].split(",")
    airport_lat_long = (float(coordinates[1].strip()),
                        float(coordinates[0].strip()))
    airport_zipcode.append((airports.loc[idx]["ident"], airport_lat_long))
    
distances = []
for combination in itertools.product(airport_zipcode, contract_zipcode):
    try:
        distance = vincenty(combination[0][1], combination[1][1]).miles
        distances.append((distance, combination[0][0], combination[1][0]))
    except:
        continue
    
distances = sorted(distances, key=lambda x:x[0])
close_by = [] 
for distance in distances:
    if distance[0] < 30:
        close_by.append(distance)

faa_codes = []
for distance in close_by:
    faa_codes.append(
        airports[airports["ident"] == distance[1]]["iata_code"].values[0]
    )

with open("faa_codes.txt", "w") as f:
    for faa_code in set(faa_codes):
        f.write(faa_code+"\n")
import code
code.interact(local=locals())
    
