"""
Date: 11/30/2022

Developers:
    - Nick Gambirasi (nag8)
    - Konstantin Kovalchuk (kk25)
    - Ben Grendaos (bgg3)

Course: CS 437 - Internet of Things - Fall 2022

Purpose:

    After running the virtualization engine, where we deployed our devices in a simulated
    world of animals, we are given the data back from the devices in a text file that
    contains json objects.

    This code parses the json files for the information that we are interested in for our
    visualizations, converts the pertinent data into pandas dataframes, then writes the
    pandas dataframes to CSV files for further analysis and visualization. 

Inputs:
    - file [-f or --file] (string) -> the filepath to the text file from the working directory
    - to_csv [-c or --to-csv] (boolean) -> whether or not to save the results of the processing
        to csv files

Outputs:
    - None: only output is csv files if the to_csv variable is true

"""

import argparse
import json
import pandas as pd
import os


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", action="store", type=str, required=True, dest="file_name", help="Filepath to sim results txt file that contains json data.")
parser.add_argument("-c", "--to-csv", action="store", type=bool, dest="to_csv", default=True, help="Boolean indicating whether or not processed data should be saved to csv files")

args = parser.parse_args()
file_name = args.file_name
to_csv = args.to_csv

# process the file into a list of json entries
print("opening file...\n")
json_dicts = []
blank_json_count = 0
with open(file_name) as f:
    # read the json data into a list
    print("collecting json entries from file...\n")
    for line in f:
        try:
            cleaned = line.strip().replace(" ", "")
            json_dicts.append(json.loads(cleaned))
        except Exception as e:
            blank_json_count = blank_json_count + 1
    
    print("Completed.")
    print(f"Skipped parsing for {blank_json_count} blank json entries.\n")

print("Iterating entries for important data...\n")
# iterate through the list of json entries and extract the pertinent information
sound_data_list =[]
pox_data_list = []
temp_data_list = []
gps_data_list = []

for json_dict in json_dicts:

    if isinstance(json_dict, list):
        for entry in json_dict:
            animal_num = entry['deviceId'].split('_')[-1] # to get the animal number
            timestamp = entry['timestamp']
            for sensor in entry['sensors']:
                sensor_ipt = sensor['input']
                if list(sensor_ipt.keys())[0] == "pulseOxygen":
                    pulse = float(sensor_ipt['pulseOxygen'][0])
                    oxy = float(sensor_ipt['pulseOxygen'][1])
                    pox_data_list.append([timestamp, animal_num, pulse, oxy])
                elif list(sensor_ipt.keys())[0] == "temperature":
                    temp = float(sensor_ipt['temperature'])
                    temp_data_list.append([timestamp, animal_num, temp])
                elif list(sensor_ipt.keys())[0] == "location":
                    gpsX = sensor_ipt['location'][0]
                    gpsY = sensor_ipt['location'][1]
                    gps_data_list.append([timestamp, animal_num, gpsX, gpsY])

print("Constructing DataFrames...\n")

# create dataframes from pertinent data
pox_df = pd.DataFrame(pox_data_list, columns=['timestamp', 'animal-id', 'pulse', 'oxygen'])
temp_df = pd.DataFrame(temp_data_list, columns=['timestamp', 'animal-id', 'temperature'])
gps_df = pd.DataFrame(gps_data_list, columns=['timestamp', 'animal-id', 'gpsX', 'gpsY'])

# write to csv files if instructed to by the parser
if to_csv:

    if not os.path.exists('CSVs'):
        os.mkdir('CSVs')

    print("Writing data to csv files...\n")
    pox_df.to_csv('CSVs/pox_data.csv', index=False)
    temp_df.to_csv('CSVs/temp_data.csv', index=False)
    gps_df.to_csv('CSVs/gps_data.csv', index=False)

else:

    print(f"Writing to csv files was set to {to_csv}\n")

print("Complete.\n")