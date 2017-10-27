# redditStalk
Generates a listing of subreddits associated with a user, submission or subreddit

## Dependencies
- [PRAW](http://praw.readthedocs.io/en/latest/)
- Optionally depends on matplotlib and [WordCloud](https://github.com/amueller/word_cloud) for the wordcloud.

## Usage

Usage: `redditstalk.py [options...] (-u USER | -s SUBREDDIT | -i ID)`
- `-h`: Displays help
- `-t`: Tab to grab users from
- `-T`: Time period to filter from
- `-l`: Submission limit
- `-cl`: Comment limit when parsing user history
- `-sl`: Scrape limit when getting comments from submission
- `-c`: Scrape users off comments
- `-w`: Generate wordcloud
- `-u`: User to stalk
- `-s`: Subreddit to scrape users from
- `-i`: Scrape users from page e.g. 39je2
- `-m`: Remove possibly superfluous messages
- `-v`: Be verbose

e.g. `redditstalk.py -s Games -cl 15 -l 20 -c -v -w`

## Example Wordcloud
![WordCloud](http://i.imgur.com/ooNsS5s.png)
