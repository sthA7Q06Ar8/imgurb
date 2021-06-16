import praw, random, webbrowser, pyimgur, os, requests

client_id = ''
client_secret = ''
user_agent = ''
imgur_id = ''
subs = []
domains = ['i.redd.it','i.imgur.com']

try:
    with open('tokens.txt') as t:
        access_token, refresh_token = t.read().strip().split()
    im = pyimgur.Imgur(imgur_id, access_token=access_token, refresh_token=refresh_token)
except FileNotFoundError:
    im = pyimgur.Imgur(imgur_id)
    webbrowser.open(im.authorization_url('pin'))
    pin = input('Enter Your Pin: ')
    access_token, refresh_token = im.exchange_pin(pin)
    with open('tokens.txt', 'w') as t:
        t.write(f'{access_token} {refresh_token}')
    
reddit = praw.Reddit(client_id=client_id,client_secret=client_secret,user_agent=user_agent)
subreddit = reddit.subreddit(random.choice(subs))
submissions = list(subreddit.top('all', limit=1000))
submissions = [submission for submission in submissions if submission.domain in domains and '.gifv' not in submission.url and submission.over_18==False]
submission = random.choice(submissions)
fileName = submission.url.replace('https://i.imgur.com/','').replace('https://i.redd.it/','')
with open(fileName,'wb') as f:
    response = requests.get(submission.url)
    f.write(response.content)
img = im.upload_image(fileName)
img.submit_to_gallery(title=submission.title)
os.remove(fileName)
