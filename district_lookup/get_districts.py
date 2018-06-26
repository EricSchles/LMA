import config
import csv
import requests


def read_data(csv_file):
    input_file = csv.DictReader(open(csv_file))
    data = []
    for row in input_file:
        data.append(row)
    return(data)


def get_address(rec):
    street = rec["Street"]
    city = rec["City"]
    state = rec["State"]
    zipcode = str(rec["Zip code"])
    if len(zipcode) == 4:
        # Fixes zipcodes where the "0" was dropped.
        zipcode = '0' + zipcode
    address = ", ".join((street, city, state)) + " " + zipcode
    # print(address)
    return(address)


def get_rep_rec(address, filters):
    url_base = 'https://www.googleapis.com/civicinfo/v2/representatives'
    api_key = config.api_key
    extras = '&'.join("{!s}={!s}".format(i[0],i[1]) for i in filters)
    url = "%s?address=%s&key=%s&%s" % (url_base, address, api_key, extras)
    print(api_key)
    print(url)
    response = requests.get(url)
    print(response)
    return(response)


if __name__ == "__main__":
    data = read_data('../../data/kft-signers_sample.csv')
    rep_records = []
    for rec in data[:5]:
        address = get_address(rec)
        # This must be a tuple, because each [0] item can have multiple instances.
        filters = (
            ('levels', 'country'),
            ('roles', 'legislatorLowerBody'),
            ('roles', 'legislatorUpperBody'),
            ('fields', 'normalizedInput,offices')
        )
        rep_rec = get_rep_rec(address, filters)
        rep_records.append(rep_rec)

    #print(rep_records)
    for rec in rep_records:
        print(rec.json())



#TODOs
# - Create state folder if it doesn't exist
# - Create file if it doesn't exist
# - Add signature to file
# - Create log of failed requests
# - Write tests
