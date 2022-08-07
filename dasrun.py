
import DASentimentalT

FILE_PATH = "./tmpdata.csv"

INDEX_MAP = {
    "depression": 0,
    "ADHD": 1,
    "Anxiety": 2,
    "depression_memes": 3,
    "adhdmeme": 4,
    "anxietymemes": 5
}

# Open data file
with open(FILE_PATH, 'rw') as data_file:

    # Get first line
    line = data_file.readline()

    # So long as there are lines left to read
    while line:

        items = line.split(",")

        this_entry = []

        for k in range(len(items)):

            if k == len(items)-1:
                break

            item = items[k]

            if not item:
                continue

            if item[0] != "[":
                continue

            if item[-1] != "]":
                item += items[k+1]

            this_entry.append(item)
        
        for k in range(len(this_entry)):
            this_entry[k] = this_entry[k][2:-2]

        # Get data of this comment
        subreddit = this_entry[0]
        author = this_entry[1]
        body = this_entry[2]

        # Get DAS score for this comment
        d, a, s = DASentimentalT.ret_results(body)

        # Store DAS in data.csv
        line = f"{line}{d},{a},{s},"
        data_file.writelines(line)
