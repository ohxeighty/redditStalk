# redditStalk
Generates a listing of subreddits associated with a user, submission or subreddit

Depends on matplotlib and WordCloud (https://github.com/amueller/word_cloud)
## Usage
usage: redditstalk.py [-h]
                      [-t {confidence,top,new,controversial,old,random,qa,live,blank}]
                      [-l LIMIT] [-cl COMMENT_LIMIT] [-sl SCRAPE_LIMIT] [-c]
                      [-w] (-u USER | -s SUBREDDIT | -i ID) [-m | -v]

e.g. redditstalk.py -s Games -cl 15 -l 20 -c -v -w  

## Example Wordcloud
![WordCloud](http://i.imgur.com/ooNsS5s.png)
