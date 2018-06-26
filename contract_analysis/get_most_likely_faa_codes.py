from uszipcode import ZipcodeSearchEngine
import pandas as pd
from geopy.distance import vincenty
import code

df = pd.read_csv("TAGGS Export 4rawnez1.ic4.csv")
contract_zipcodes = df["ZIP Code"].unique().astype(str)
airports = pd.read_csv("airport_codes.csv")
airports = airports[(airports["type"] == "small_airport")
                    | (airports["type"] == "medium_airport")
                    | (airports["type"] == "large_airport")]
code.interact(local=locals())

for contract_zipcode in contract_zipcodes:
    search = ZipcodeSearchEngine()
    zipcode = search.by_zipcode(contract_zipcode)
    # = (zipcode["Latitude"], zipcode["Longitude"])
