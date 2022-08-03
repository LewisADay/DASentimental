# To parse json data

import json
import os


# Parse large json files by yeilding one item at a time
def read_large_json_to_str(file, max_lnum=100):
    curly_idx = []
    jstr = ""
    first_curly_found = False
    with open(file, 'r') as fp:
        #Reading file line by line
        line = fp.readline()
        lnum = 0
        while line:
            for a in line:
                if a == '{':
                    curly_idx.append(lnum)
                    first_curly_found = True
                elif a == '}':
                    try:
                        curly_idx.pop()
                    except:
                        print(jstr)
                        print(line)

            # when the right curly for every left curly is found,
            # it would mean that one complete data element was read
            if len(curly_idx) == 0 and first_curly_found:
                jstr = f'{jstr}{line}'
                jstr = jstr.rstrip()
                jstr = jstr.rstrip(',')
                jstr[:-1]
                print("------------")
                if len(jstr) > 10:
                    print("making json")
                    j = json.loads(jstr)
                yield jstr
                jstr = ""
                line = fp.readline()
                lnum += 1
                continue

            if first_curly_found:
                jstr = f'{jstr}{line}'

            line = fp.readline()
            lnum += 1
            if lnum > max_lnum:
                break

# Set paths
FILE_PATH = "./RC_2018-01"
DATA_PATH = "./Data/"
out_file_path = "./data.csv"

# State the columns of the entry we want
wanted_columns = ["author", "body", "subreddit"]

# Read each entry of the dataset
for entry in read_large_json_to_str(FILE_PATH):

    # Make that entry a dict of json fields
    data = json.loads(entry)

    # If the comment has been removed, ignore
    if data["body"] == "[removed]":
        continue

    # Select only those columns from the entry
    wanted_data = {key:[data[key]] for key in data if key in wanted_columns}
    wanted_data = [wanted_data[key] for key in wanted_data]

    # Open output file to append to
    with open(out_file_path, 'a') as out_file:
    
        # For each datapoint we want add entry to csv
        for data in wanted_data:
            out_file.write(f"{data},")

        # Add new line to end this entry
        out_file.write(f"\n")


