import requests
import json
import csv
from tqdm import *

def addresses_from_csv(path=None, column=None):
        
    addresses = []

    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            addresses.append(row[column])
            
    return addresses
  
# Get addresses from CSV
addresses = addresses_from_csv(path='path/to/your/file.csv', column=0)

# Set Google Maps API key
api_key = YOUR_API_KEY

# Initialize array for transformed addresses
transformed = []
transformed.append(['Country', 'Post code', 'City', 'Street & No'])

for query in tqdm(addresses):
    
    # API call, storing information as JSON
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + query + '&lang=en&key=' + api_key
    r = requests.get(url)
    data = r.json()
    #print(data)
    
    # clear all values to avoid appending values from previous iterations a second time
    number = street = country = postal_code = city = '' 
    
    # looping over address components in JSON
    for component in data['results'][0]['address_components']:
        if 'street_number' in component['types']:
            number = component['long_name']
        elif 'route' in component['types']:
            street = component['long_name']
        elif 'country' in component['types']:
            country = component['long_name']
        elif 'postal_code' in component['types']:
            postal_code = component['long_name']
        elif 'locality' in component['types']:
            city = component['long_name']
        elif 'postal_town' in component['types']:
            city = component['long_name']
        else:
            continue

    street_and_no = street + ' ' + number
    transformed.append([country, postal_code, city, street_and_no])
    
with open('transformed_addresses.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for row in transformed:
        writer.writerow(row)

print('done')
