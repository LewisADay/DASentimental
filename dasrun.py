
import DASentimentalT
from tabulate import tabulate

FILE_PATH = "./tmpdata.csv"

INDEX_MAP = {
    "depression": 0,
    "ADHD": 1,
    "Anxiety": 2,
    "depression_memes": 3,
    "adhdmeme": 4,
    "anxietymemes": 5
}

counter_comments = [0, 0, 0, 0, 0, 0]

depression_scores = [0, 0, 0, 0, 0, 0]
anxiety_scores = [0, 0, 0, 0, 0, 0]
stress_scores = [0, 0, 0, 0, 0, 0]

# Open data file
with open(FILE_PATH, 'r+') as data_file:

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

        # Collate the scores
        depression_scores[INDEX_MAP[subreddit]] += d
        anxiety_scores[INDEX_MAP[subreddit]] += a
        stress_scores[INDEX_MAP[subreddit]] += s

        # Increment counter
        counter_comments[INDEX_MAP[subreddit]] += 1

        # Get next line
        line = data_file.readline()


for subreddit in INDEX_MAP:
    if counter_comments[INDEX_MAP[subreddit]] == 0:
        continue
    depression_scores[INDEX_MAP[subreddit]] = depression_scores[INDEX_MAP[subreddit]] / counter_comments[INDEX_MAP[subreddit]]
    anxiety_scores[INDEX_MAP[subreddit]] = anxiety_scores[INDEX_MAP[subreddit]] / counter_comments[INDEX_MAP[subreddit]]
    stress_scores[INDEX_MAP[subreddit]] = stress_scores[INDEX_MAP[subreddit]] / counter_comments[INDEX_MAP[subreddit]]

tmp = [
    [
        subreddit,
        f"{depression_scores[INDEX_MAP[subreddit]]:.2f}",
        f"{anxiety_scores[INDEX_MAP[subreddit]]:.2f}",
        f"{stress_scores[INDEX_MAP[subreddit]]:.2f}"
    ]
    for subreddit in INDEX_MAP
]

print(tabulate(tmp, headers = ["Subreddit", "Avg. D", "Avg. A", "Avg. S"]))

