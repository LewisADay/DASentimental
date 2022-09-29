# LewisADay/DASentimental

A fork of asrafaiz7/DASentimental, using DASentimental to perform basic sentiment analysis on a dataset of Reddit comments from various mental health related subreddits and their `meme' subreddit equivalents. The subsequent analysis showed that the meme subreddits tend to have broadly similar DAS scores to their more serious counterparts, though all the meme subreddits score less in the Depression metric, indicating, as one might expect, that a forum rife with jokes, is a slightly cheerier place that a forum for discussion on the same topic.

### Dataset

The source for the dataset was https://files.pushshift.io/reddit/comments/, from which the dataset for Jan-Mar 2020 was used in this project. As we are only interested in select subreddits we then filtered the dataset and extracted the relevant comments into the dataset found in tmpdata.json. To understand the format of the data the creators of the dataset provided sample_data.json, which demonstrates the format and style of the data, without needing to manage dealing with enormous json files.

### Use

This project was intended for single use and single output, it is, therefore, not designed to be scalable or easilly useable. Instructions for its use are, therefore, ommitted, as I can scarcely recall the exact order of operations and intermediate steps which are not obvious from the repository itself. If you wish to perform similar work, please see asrafaiz7/DASentimental, for how to use DASentimental for your own analysis.
