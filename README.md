# redditStalk
Generates a listing of subreddits associated with a user, submission or subreddit
## Usage
usage: redditstalk.py [-h]
                      [-t {confidence,top,new,controversial,old,random,qa,live,blank}]
                      [-l LIMIT] [-cl COMMENT_LIMIT] [-sl SCRAPE_LIMIT] [-c]
                      [-w] (-u USER | -s SUBREDDIT | -i ID) [-m | -v]

Stalk people and view their visited subreddits

optional arguments:
  -h, --help            show this help message and exit
  -t {confidence,top,new,controversial,old,random,qa,live,blank}, --tab {confidence,top,new,controversial,old,random,qa,live,blank}
                        grab users from which tab
  -l LIMIT, --limit LIMIT
                        submission limit
  -cl COMMENT_LIMIT, --comment_limit COMMENT_LIMIT
                        comment limit when parsing user history
  -sl SCRAPE_LIMIT, --scrape_limit SCRAPE_LIMIT
                        scrape limit when getting comments from submission
  -c, --comments        scrape users off comments
  -w, --wordcloud       generate wordcloud
  -u USER, --user USER  user to stalk
  -s SUBREDDIT, --subreddit SUBREDDIT
                        subreddit to scrape users from
  -i ID, --id ID        scrape users from page e.g. 39je2
  -m, --minimal         removes possibly superflous messages
  -v, --verbose         adds verbosity (many prints may slow program)

