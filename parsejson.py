# To parse json data

import json

# Set paths
FILE_PATH = "./sample_data.json"
#FILE_PATH = "./RC_2018-01.json"
#DATA_PATH = "./Data/"
out_file_path = "./data.csv"

# State the columns of the entry we want
wanted_columns = ["subreddit", "author", "body"]

# State the subreddits we want
wanted_subreddits = ["ADHD", "adhdmeme", "Anxiety", "anxietymemes", "depression", "depression_memes"]

# open source file
with open(FILE_PATH, 'r') as source_file:

    line = source_file.readline()

    # Read each entry of the dataset
    while line:

        print(line)

        # Remove any trailing whitespace
        line = line.rstrip()

        # Remove new line char
        line = line.rstrip("\n")

        # Make that entry a dict of json fields
        data = json.loads(line)

        # If the comment has been removed, ignore
        if data["body"] == "[removed]" or data["body"] == "[deleted]":
            line = source_file.readline()
            continue

        # Determine if comment pertains to wanted subreddit
        if data["subreddit"] not in wanted_subreddits:
            line = source_file.readline()
            continue

        # Select only those columns from the entry
        wanted_data = {key:[data[key]] for key in data if key in wanted_columns}
        #wanted_data = [wanted_data[key] for key in wanted_data]

        # Open output file to append to
        with open(out_file_path, 'a') as out_file:
        
            # For each datapoint we want add entry to csv
            for column in wanted_columns:
                out_file.write(f"{wanted_data[column]},")

            # Add new line to end this entry
            out_file.write(f"\n")

        # Read the next line
        line = source_file.readline()
