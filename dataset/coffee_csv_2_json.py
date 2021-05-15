#!/user/bin/env python3 -tt
"""
Converts a comma-separated CSV file with a coffee data records into a hierarchically organized JSON document.
"""

import sys
import argparse
import os.path
import simplejson as json
import csv
from decimal import Decimal
import pprint

# Global variables

# Class declarations

class CoffeeCsvRecord:

    def __init__(self, roastery, name, priceEurKg, arabica, robusta, strength, caffeine, roastLevel, crema):
        self.roastery = roastery
        self.name = name
        self.priceEurKg = priceEurKg
        self.arabica = arabica
        self.robusta = robusta
        self.strength = strength
        self.caffeine = caffeine
        self.roastLevel = roastLevel
        self.crema = crema

    def hierarchic(self):

        record = {}

        record["roastery"] = str(self.roastery).strip()
        record["name"] = str(self.name).strip()
        record["priceEurKg"] = self.str2decimal(self.priceEurKg)

        blend = {}
        blend["arabica"] = self.str2decimal(self.arabica)
        blend["robusta"] = self.str2decimal(self.robusta)
        record["blend"] = blend

        taste = {}
        taste["strength"] = self.str2decimal(self.strength)
        taste["caffeine"] = self.str2decimal(self.caffeine)
        taste["roastLevel"] = self.str2decimal(self.roastLevel)
        taste["crema"] = self.str2decimal(self.crema)
        record["taste"] = taste
        
        return record

    def str2decimal(self, str):
        return Decimal(str.replace(',','.').strip())

# Function declarations

def convert(inFilepath, outFilepath):

    with open(inFilepath) as inFileCsv:

        csvReader = csv.reader(inFileCsv, delimiter=',')

        lineCount = 0
        jsonRecords = []

        for row in csvReader:

            if lineCount == 0:
                # skip header
                lineCount += 1
            else:
                coffeeCsvRecord = CoffeeCsvRecord(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                jsonRecords.append(coffeeCsvRecord.hierarchic())
                lineCount += 1
        
        print(f'processed {lineCount-1} coffee CSV records')
        print(f'generated {len(jsonRecords)} coffee JSON records')

        jsonStr = json.dumps(jsonRecords, indent=2, ensure_ascii=False)
        print("json: ", jsonStr)

        with open(outFilepath, 'w') as outFileJson:
            outFileJson.write(jsonStr)        

# main
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Coffee Record CSV to JSON Converter')

    parser.add_argument('-i','--in', help='Input CSV file', required=True)
    parser.add_argument('-o','--out', help='Output JSON file', required=True)

    args = vars(parser.parse_args())
    print('args:', json.dumps(args, indent=2))

    if not os.path.isfile(args['in']):
        sys.exit(f"input file {args['in']} does not exist")

    if os.path.isfile(args['out']):
        sys.exit(f"output file {args['out']} already exists")    

    convert(args['in'], args['out'])

    print("done")