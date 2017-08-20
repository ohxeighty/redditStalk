import praw 
import argparse 
import collections

def info(text):
   print "[*] " + text
   
def warning(text):
   print "[!] " + text 
   
def error(text):
   print "[-] " + text 
  
def success(text):
   print "[+] " + text 

def display_wordcloud(string):
   try:
      info("Creating wordcloud") 
      from wordcloud import WordCloud
      import matplotlib.pyplot as plt 
      wordcloud = WordCloud(width=3200, height=1600).generate(string)
      # Run as administrator buddy-o-pal
      plt.imshow(wordcloud, interpolation='bilinear')
      plt.axis("off")
      plt.show()
   except:  
      error("Could not create wordcloud, check if you have matplotlib and wordcloud")
  
subreddit_type = ["controversial", "gilded", "hot", "new", "rising", "top"]   
subreddit_type = ["confidence", "top", "new", "controversial", "old", "random", "qa", "live", "blank"]
parser = argparse.ArgumentParser(description="Stalk people and view their visited subreddits")
parser.add_argument('-t', '--tab', help="grab users from which tab", required = False, default = "hot", choices=subreddit_type)
parser.add_argument('-l', '--limit', type=int, help="submission limit", required = False, default = 10)
parser.add_argument('-cl', '--comment_limit', type=int, help="comment limit when parsing user history", required = False, default = 10)
parser.add_argument('-sl', '--scrape_limit', type=int, help="scrape limit when getting comments from submission", required = False, default = 10)
parser.add_argument('-c', '--comments', help="scrape users off comments", required = False, default = False, action="store_true")
parser.add_argument('-w', '--wordcloud', help="generate wordcloud", required = False, default = False, action="store_true")

selection = parser.add_mutually_exclusive_group(required=True)
selection.add_argument('-u', '--user', help ="user to stalk", required = False, default = None)
selection.add_argument('-s', '--subreddit', help ="subreddit to scrape users from", required = False, default = None)
selection.add_argument('-i', '--id', help="scrape users from page e.g. 39je2", required = False, default = None)

verbosity = parser.add_mutually_exclusive_group(required=False)
verbosity.add_argument('-m', '--minimal', help="removes possibly superflous messages", required = False, default = False, action="store_true")
verbosity.add_argument('-v', '--verbose', help="adds verbosity (many prints may slow program)", required = False, default = False, action="store_true")

args = parser.parse_args()
# read only, add parameters username and password for write
reddit = praw.Reddit(client_id="ID_HERE",
                     client_secret="SECRET_HERE",
                     user_agent="redditstalk"
                     ) 
         
if args.subreddit:
   info("Getting Subreddit")
   subreddit = reddit.subreddit(args.subreddit)
   if not subreddit:
      raise Exception("Subreddit not found")
   if not args.minimal:
      print subreddit.display_name
      print subreddit.title
      print("Description: " + subreddit.description).encode('utf-8')
   
   # gib switch pls 
   info("Getting Submissions")
   if args.tab == "hot":
      submissions = [x for x in subreddit.hot(limit=args.limit)]
   elif args.tab == "controversial":
      submissions = [x for x in subreddit.controversial(limit=args.limit)]
   elif args.tab == "gilded":
      submissions = [x for x in subreddit.gilded(limit=args.limit)]
   elif args.tab == "new":
      submissions = [x for x in subreddit.new(limit=args.limit)]
   elif args.tab == "rising":
      submissions = [x for x in subreddit.rising(limit=args.limit)]
   elif args.tab == "top":
      submissions = [x for x in subreddit.top(limit=args.limit)]
   
   info("Iterating over submissions")
   
   redditor_list = [] 
   
   for i in submissions:
      try:
         redditor = i.author
         redditor_list.append(redditor)
         if args.verbose:
            # Encode to avoid bad mapping errors ,_,
            print("Submission Title: " + i.title).encode('utf-8') 
            print "Submission Score: " + str(i.score)
            print "Submission ID: " + i.id 
            print "Submission URL: " + i.url 
            print "Author: " + redditor.name
      except:
         error("Error reading submission")
      
      if args.comments:
         # Remove "More Comments" instance 
         i.comments.replace_more(limit=0)
         # Flat list of comments 
         for comment in i.comments.list()[:args.scrape_limit]:
            try:
               redditor_list.append(comment.author)
               if args.verbose:
                  print("Comment: " + comment.body).encode('utf-8')
            except: 
               error("Error reading submission comment")
               
   info("Parsing redditor list") 
   # lazyhacks.com 
   redditor_list = list(set(redditor_list))
   info("Number of Redditors to parse: " + str(len(redditor_list)))
   
   subreddits = []
   for redditor in redditor_list:
      try:
         comments = redditor.comments.new(limit=args.comment_limit)
      except:
         error("Error reading redditor profile, possibly private")
      try:
         temp = []
         for comment in comments:
            temp.append(comment.subreddit.display_name)
            if args.verbose:
                  print("Comment: " + comment.body).encode('utf-8')
                  print("Author: " + redditor.name).encode('utf-8')
         # unique subreddits per user 
         temp = list(set(temp))
         subreddits.extend(temp)
      except:
         error("Error reading comment from profile")
      # append string to subreddit for wordcloud compat :^)
   
   
   # Print and finish
   success("||||| Finished - Displaying Results |||||")
   count = collections.Counter(subreddits)
   total = sum([i for i in count.values()]) * 1.0
   for i,v in count.most_common():
      print("Subreddit Name: " + i).encode('utf-8')
      print("Subreddit Frequency: " + str(v)).encode('utf-8')
      print("Subreddit Percentage: " + str( round((v / total)*100, 2)) + "\n").encode('utf-8')
   
   
   if args.wordcloud:
      display_wordcloud(' '.join(subreddits))
   
    
elif args.user:
   if not args.minimal:
      print "Redditor: " + args.user 
      
   redditor = reddit.redditor(args.user)
   if not redditor:
      raise Exception("Redditor not found")
   subreddits = []
   try:
      comments = redditor.comments.new(limit=args.comment_limit)
   except:
      error("Error reading redditor profile, possibly private")
   
   for comment in comments:
      try:
         subreddits.append(comment.subreddit.display_name)
         if args.verbose:
               print("Comment: " + comment.body).encode('utf-8')
               print("Author: " + redditor.name).encode('utf-8')
      except:  
         error("Error reading comment from profile")
         
   # Print and finish
   success("||||| Finished - Displaying Results |||||")
   count = collections.Counter(subreddits)
   total = sum([i for i in count.values()]) * 1.0
   for i,v in count.most_common():
      print("Subreddit Name: " + i).encode('utf-8')
      print("Subreddit Frequency: " + str(v)).encode('utf-8')
      print("Subreddit Percentage: " + str( round((v / total)*100, 2)) + "\n").encode('utf-8')
   
   
   if args.wordcloud:
      display_wordcloud(' '.join(subreddits))
# Grab comments from page automatically
elif args.id:
   redditor_list = [] 
   i = reddit.submission(id=args.id)
   if not i:
      raise Exception("Submission not found")
   try:
      redditor = i.author
      redditor_list.append(redditor)
      if args.verbose:
         # Encode to avoid bad mapping errors ,_,
         print("Submission Title: " + i.title).encode('utf-8') 
         print "Submission Score: " + str(i.score)
         print "Submission ID: " + i.id 
         print "Submission URL: " + i.url 
         print "Author: " + redditor.name
   except:
      error("Error reading submission")
   
   if args.comments:
      # Remove "More Comments" instance 
      i.comments.replace_more(limit=0)
      # Flat list of comments 
      for comment in i.comments.list()[:args.scrape_limit]:
         try:
            redditor_list.append(comment.author)
            if args.verbose:
               print("Comment: " + comment.body).encode('utf-8')
         except: 
            error("Error reading submission comment")
            
            
   info("Parsing redditor list") 
   redditor_list = list(set(redditor_list))
   info("Number of Redditors to parse: " + str(len(redditor_list)))
   subreddits = []
   for redditor in redditor_list:
      try:
         comments = redditor.comments.new(limit=args.comment_limit)
      except:
         error("Error reading redditor profile, possibly private")
      try:
         temp = []
         for comment in comments:
            temp.append(comment.subreddit.display_name)
            if args.verbose:
                  print("Comment: " + comment.body).encode('utf-8')
                  print("Author: " + redditor.name).encode('utf-8')
         # unique subreddits per user 
         temp = list(set(temp))
         subreddits.extend(temp)
      except:
         error("Error reading comment from profile")
      
      
   # Print and finish
   success("||||| Finished - Displaying Results |||||")
   count = collections.Counter(subreddits)
   total = sum([i for i in count.values()]) * 1.0
   for i,v in count.most_common():
      print("Subreddit Name: " + i).encode('utf-8')
      print("Subreddit Frequency: " + str(v)).encode('utf-8')
      print("Subreddit Percentage: " + str( round((v / total)*100, 2)) + "\n").encode('utf-8')
   
   
   if args.wordcloud:
      display_wordcloud(' '.join(subreddits))