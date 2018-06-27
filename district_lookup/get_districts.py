import csv
import logging
import requests

from config import API_KEY
from datetime import datetime
from os import mkdir


output_folder = '../../signature_output/'
# source_data = '../../data/kft-signers_sample.csv'
source_data = '../../data/kft-signers.csv'
logging_level = logging.DEBUG


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
    extras = '&'.join("{!s}={!s}".format(i[0], i[1]) for i in filters)
    url = "%s?address=%s&key=%s&%s" % (url_base, address, API_KEY, extras)

    # if oauth:
    #     auth = OAuth1(API_KEY, API_SECRET, CLIENT_ID, CLIENT_SECRET)
    #     response = requests.get(url, auth=auth)

    # else:
    response = requests.get(url)
    print(url)
    print(response)
    return(response)


def create_signature(rec, address):
    """

    Output is a string
    Example output: `John Doe, 123 Sunny Lane, FL 34207`

    """
    first = rec['First Name ']
    last = rec['Last Name']
    signature = "%s %s, %s" % (first, last, address)
    return(signature)


def extract_jurisdictions(rep_rec):
    """

    Output is list of offices where address is.
    Example output:
        ['VA-Sen', 'VA-08-Rep']
        ['IL-Sen', 'IL-06-Rep']
        ['NY-Sen', 'NY-27-Rep']

    """
    try:
        offices = rep_rec.json()['offices']
        jurisdictions = []
        for office in offices:
            office_text = ''
            o_name = office['name']
            if o_name == 'United States Senate':
                state = office['divisionId'][-2:]
                office_text = state.upper() + '-' + "Sen"
            else:
                text = 'United States House of Representatives '
                district = o_name.lstrip(text)
                office_text = district + '-' + "Rep"
            jurisdictions.append(office_text)
        return(jurisdictions)
    except Exception as e:
        logging.error('Error: %s' % rep_rec, exc_info=e)


if __name__ == "__main__":

    # Create timestamped folders
    now = datetime.now
    time_of_run = '{}'.format(now().strftime('%Y-%m-%d-%H%M%S'))
    output_folder = output_folder + time_of_run + '/'
    mkdir(output_folder)
    log_file = output_folder + 'output.log'
    logging.basicConfig(filename=log_file, level=logging_level)

    # Read and process data
    data = read_data(source_data)
    rep_records = []
    count = 1
    for rec in data:
        address = get_address(rec)

        # Must be a tuple, because each [0] item can have multiple instances.
        filters = (
            ('levels', 'country'),
            ('roles', 'legislatorLowerBody'),
            ('roles', 'legislatorUpperBody'),
            ('fields', 'normalizedInput,offices')
        )
        rep_rec = get_rep_rec(address, filters)
        jurisdictions = extract_jurisdictions(rep_rec)
        signature = create_signature(rec, address)


        # Write lines out to files in folder
        try:
            for j in jurisdictions:
                file_name = output_folder + j + '.txt'
                f = open(file_name, "a+")
                f.write(signature)
                f.write('\n')
                f.close()
        except:
            print('############### Error!!!!!!!!!!!!!!!!! ############')

        count += 1
        print(count)
        # # Pulling back on API, to try to reduce errors.
        #
        # if count % 25 == 0:
        #     time.sleep(1)



#TODOs

# - Check for duplicate signatures
# - Check logs for requests and resulted in errors
# - Write tests

#Resources
# - List of congressional members -- https://github.com/unitedstates/congress-legislators
