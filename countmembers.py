
import numpy as np


FILE_PATH = "./data.csv"

INDEX_MAP = {
    "depression": 0,
    "ADHD": 1,
    "Anxiety": 2,
    "depression_memes": 3,
    "adhdmeme": 4,
    "anxietymemes": 5
}

counter_comments = [0, 0, 0, 0, 0, 0]
counter_unique_authors = [0, 0, 0, 0, 0, 0]

member_lists = [[], [], [], [], [], []]

author_contributions = {}

total_comments = 0

# Open data file
with open(FILE_PATH) as data_file:

    # Get first line
    line = data_file.readline()

    # So long as there are lines left to read
    while line:

        total_comments += 1

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

        # Increment comment counter
        counter_comments[INDEX_MAP[subreddit]] += 1

        # Add this comment to this authors contributions
        if author not in author_contributions:
            author_contributions[author] = {sr: 0 for sr in INDEX_MAP}
        author_contributions[author][subreddit] += 1

        # Determine if this is a new unique author for this subreddit
        if author not in member_lists[INDEX_MAP[subreddit]]:
            counter_unique_authors[INDEX_MAP[subreddit]] += 1
            member_lists[INDEX_MAP[subreddit]].append(author)

        line = data_file.readline()

# Calculate total number of authors
total_authors = len(author_contributions)

## Get per author stats
# Average comments per author
average_author_comments = total_comments / total_authors

# Average comments per author per subreddit
average_author_per_subreddit_comments = [0, 0, 0, 0, 0, 0]

for author in author_contributions:
    subreddits = author_contributions[author]

    # Contribute to averages
    for subreddit in subreddits:
        average_author_per_subreddit_comments[INDEX_MAP[subreddit]] += subreddits[subreddit]

# Average the per subreddit comments
for k in range(len(average_author_per_subreddit_comments)):
    if counter_unique_authors[k] != 0:
        average_author_per_subreddit_comments[k] = average_author_per_subreddit_comments[k] / counter_unique_authors[k]

print(f"Total comments: {total_comments}")
print(f"Total authors: {total_authors}")
print(f"Average number of comments per author: {average_author_comments}")
"""padding_size = max(map(lambda x: len(x), [key for key in INDEX_MAP]))
s = "Subreddit"
while len(s) < padding_size:
    s += " "
print(f"{s}\t|\tAvg.\t|\tComments\t|\tAuthors")"""

tmp = [
    [
        subreddit,
        f"{average_author_per_subreddit_comments[INDEX_MAP[subreddit]]:.2f}",
        f"{counter_comments[INDEX_MAP[subreddit]]:d}",
        f"{counter_unique_authors[INDEX_MAP[subreddit]]:d}"
    ]
    for subreddit in INDEX_MAP
]

from tabulate import tabulate

print(tabulate(tmp, headers = ["Subreddit", "Avg.", "Comments", "Authors"]))

"""
for subreddit in INDEX_MAP:
    str = f"{average_author_per_subreddit_comments[INDEX_MAP[subreddit]]:.2f}"
    str = f"{str}\t|\t{counter_comments[INDEX_MAP[subreddit]]:d}"
    str = f"{str}\t|\t{counter_unique_authors[INDEX_MAP[subreddit]]:d}"
    while len(subreddit) < padding_size:
        subreddit += " "
    str = f"{subreddit}\t|\t{str}"
    print(str)
"""