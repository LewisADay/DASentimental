
from tabulate import tabulate
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

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

tmp = [
    [
        subreddit,
        f"{average_author_per_subreddit_comments[INDEX_MAP[subreddit]]:.2f}",
        f"{counter_comments[INDEX_MAP[subreddit]]:d}",
        f"{counter_unique_authors[INDEX_MAP[subreddit]]:d}"
    ]
    for subreddit in INDEX_MAP
]

print(tabulate(tmp, headers = ["Subreddit", "Avg.", "Comments", "Authors"]))

subreddit_pairs = []

for s1 in INDEX_MAP:
    for s2 in INDEX_MAP:
        if s1 == s2:
            continue
        if [s1, s2] in subreddit_pairs or [s2, s1] in subreddit_pairs:
            continue
        subreddit_pairs.append([s1, s2])

subreddit_pairs = np.array(subreddit_pairs)
counter_shared_authors = np.zeros(shape=subreddit_pairs.shape)

for author in author_contributions:
    subreddits = author_contributions[author]

    for s1 in [key for key in subreddits if subreddits[key] != 0]:
        for s2 in [key for key in subreddits if subreddits[key] != 0]:
            if s1 == s2:
                continue

            if [s1, s2] in subreddit_pairs:
                counter_shared_authors[subreddit_pairs == [s1, s2]] += 1

            if [s2, s1] in subreddit_pairs:
                counter_shared_authors[subreddit_pairs == [s2, s1]] += 1

G = nx.empty_graph(6)

edge_sizes = counter_shared_authors / total_authors
edge_sizes = edge_sizes * 1000

for [s1, s2] in subreddit_pairs:
    weight = edge_sizes[subreddit_pairs == [s1, s2]]
    G.add_weighted_edges_from([(INDEX_MAP[s1], INDEX_MAP[s2]), weight])

node_sizes = np.array(counter_unique_authors) / total_comments
node_sizes = node_sizes * 1000
nx.draw_networkx_nodes(G, pos=nx.spring_layout(G), node_size=node_sizes)

for [s1, s2] in subreddit_pairs:
    weight = edge_sizes[subreddit_pairs == [s1, s2]]
    nx.draw_networkx_edges(G, pos=nx.spring_layout(G), edgelist=[(INDEX_MAP[s1], INDEX_MAP[s2])], width=weight/10)

nx.draw_networkx_labels(G, pos=nx.spring_layout(G), labels={INDEX_MAP[lab]: f"r/{lab}" for lab in INDEX_MAP})

plt.show()
