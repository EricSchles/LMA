import csv
import logging
import os
import requests
import time

from collections import defaultdict
from config import API_KEY
from datetime import datetime


output_folder = '../../signature_output/'
# source_data = '../../data/kft-signers_sample.csv'
source_data = '../../data/kft-signers.csv'
logging_level = logging.INFO
error_count = 0

header_text = 'The following individuals signed the Lawyers Moms of America \
open letter dated June 29, 2018, which demands a just and humane resolution \
to the ongoing crisis of families seeking asylum in the U.S. being separated \
or detained at the border. To read the letter, visit: \
https://lawyermomsofamerica.squarespace.com/openletter/\n\
\n\
\n\
Signers located in your district\n\
----------------------------------\n\
'


def read_data(csv_file):
    input_file = csv.DictReader(open(csv_file))
    data = []
    for row in input_file:
        data.append(row)
    return(data)


def get_address(rec):
    street = rec["Street"].strip()
    city = rec["City"].strip()
    state = rec["State"].strip()
    zipcode = str(rec["Zip code"]).strip()

    if len(zipcode) == 4:
        # Fixes zipcodes where the "0" was dropped.
        zipcode = '0' + zipcode

    address = ", ".join((street, city, state)) + " " + zipcode

    street_no_apt = None
    address_no_apt = address
    if "#" in street:
        x = street.split('#')
        street_no_apt = x[0].strip()
        address_no_apt = ", ".join((street_no_apt, city, state)) + " " + zipcode


    # print(address)
    return(address, address_no_apt)


def get_rep_rec(address, filters):
    """

    Returns http response object.

    """

    url_base = 'https://www.googleapis.com/civicinfo/v2/representatives'
    extras = '&'.join("{!s}={!s}".format(i[0], i[1]) for i in filters)
    url = "%s?address=%s&key=%s&%s" % (url_base, address, API_KEY, extras)

    response = requests.get(url)
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
        logging.error('############## Error!!!!!!!!!!!!!!!!! ###########')
        logging.error('Error: %s' % rep_rec, exc_info=e)
        logging.error(rep_rec.url)
        logging.error(rep_rec.status_code)
        global error_count
        error_count += 1


def remove_duplicates(data):
    '''

    Some people signed twice. We need to remove those.
    Oh god, this is so messy, but I was deadline.

    '''

    emails = set()

    cleaned_data = [dict(i) for i in data[:]]

    for rec in data:
        email = rec["Email Address"].strip().lower()
        first = rec["First Name "].strip().lower()
        last = rec["Last Name"].strip().lower()

        if email in emails:

            for rec1 in data:
                email1 = rec1["Email Address"].strip().lower()
                # If emails match
                if email1 == email:

                    # Pull the name and zip
                    first1 = rec1["First Name "].strip().lower()
                    last1 = rec1["Last Name"].strip().lower()
                    zipcode1 = rec1["Zip code"].strip().lower()
                    timestamped1 = rec1["Timestamp"]

                    # Addition info to pull from the first record
                    zipcode = rec["Zip code"].strip().lower()
                    timestamped = rec["Timestamp"]

                    if (first, last, zipcode) == (first1, last1, zipcode1):
                        if timestamped1 != timestamped:
                            logging.debug("Duplicate record found------------")
                            logging.debug("First record:")
                            address, x = get_address(rec)

                            logging.debug((first, last, zipcode, email,
                                          timestamped, address))

                            logging.debug("Second record:")
                            address1, x1 = get_address(rec1)

                            logging.debug((first1, last1, zipcode1, email1,
                                          timestamped1, address1))

                            if dict(rec1) in cleaned_data:
                                cleaned_data.remove(dict(rec1))

        emails.add(email)

    logging.info("Length of original data: %s" % len(data))
    logging.info("Length of cleaned data: %s" % len(cleaned_data))

    return(cleaned_data)


if __name__ == "__main__":

    now = datetime.now
    start = now()

    # Create timestamped folders
    time_of_run = '{}'.format(now().strftime('%Y-%m-%d-%H%M%S'))
    output_folder = output_folder + time_of_run + '/'
    os.mkdir(output_folder)
    log_file = output_folder + 'output.log'
    logging.basicConfig(filename=log_file, level=logging_level)
    logging.info('----------------------------------------------------- NEW RUN -------------------------------------------')
    logging.info(start)

    # Read and process data
    data = read_data(source_data)
    data = remove_duplicates(data)

    rep_records = []
    status_counts = defaultdict(int)
    count = 1
    for rec in data[:1000]:
        address, address_no_apt = get_address(rec)

        # Must be a tuple, because each [0] item can have multiple instances.
        filters = (
            ('levels', 'country'),
            ('roles', 'legislatorLowerBody'),
            ('roles', 'legislatorUpperBody'),
            ('fields', 'normalizedInput,offices')
        )
        rep_rec = get_rep_rec(address_no_apt, filters)
        jurisdictions = extract_jurisdictions(rep_rec)
        signature = create_signature(rec, address)

        # Write lines out to files in folder
        try:
            for j in jurisdictions:
                file_name = output_folder + j + '.txt'

                if os.path.isfile(file_name):
                    f = open(file_name, "a+")
                else:
                    f = open(file_name, "a+")
                    f.write(header_text)

                f.write(signature)
                f.write('\n')
                f.close()
        except Exception as e:
            logging.error('############## Error!!!!!!!!!!!!!!!!! ###########')
            logging.error('address: %s' % address)
            logging.error('%s, %s' % (rep_rec, rep_rec.url))
            logging.error('Error: %s' % rep_rec, exc_info=e)
            error_count += 1

        status_counts[rep_rec.status_code] += 1

        count += 1

        # Pulling back on API, to try to reduce errors.
        if count % 50 == 0:
            logging.info("Total: %s" % count)
            print("Total: %s" % count)
            logging.info("Errors: %s" % error_count)
            print("Errors: %s" % error_count)
            logging.info("HTTP Status counts: %s" % status_counts)
            print("HTTP Status counts: %s" % status_counts)
            time.sleep(3)

    end = datetime.now()
    logging.info(end)
    time_diff = end - start
    logging.info(time_diff)
    logging.info((time_diff.min, time_diff.seconds))


# TODOs
# - Write tests

# Resources
# List of congressional members --
# https://github.com/unitedstates/congress-legislators
