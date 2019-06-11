import os
import json
import random
import twitter
import psycopg2
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials

c_key = os.environ["TWITTER_CONSUMER_KEY"]
c_secret = os.environ["TWITTER_CONSUMER_SECRET"]
a_token_key = os.environ["TWITTER_ACCESS_KEY"]
a_token_secret = os.environ["TWITTER_ACCESS_SECRET"]

api = twitter.Api(c_key, c_secret, a_token_key, a_token_secret)

conn = psycopg2.connect(os.environ["DATABASE_URL"], sslmode='require')
cur = conn.cursor()

cur.execute("SELECT * FROM index;")
image_index = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM images;")
url_count = cur.fetchone()[0]

if (url_count == 0 or url_count < image_index):

  print("FETCHING NEW URLS")
  client = ImageSearchAPI(CognitiveServicesCredentials(os.environ["BING_KEY"]))

  image_results = []
  image_results.extend(client.images.search(query="cute dog").value)
  image_results.extend(client.images.search(query="puppies").value)

  for image in image_results:
    cur.execute("INSERT INTO images(url) VALUES(%s)", [image.content_url])

  conn.commit()

# tweeted = False

# while not tweeted:
#   try:
#     url = url_list[image_index]
#     image_index += 1
#     print("Attempting tweet of image url: {}".format(url))
#     api.PostUpdate(". @CarterAlzamora @Houghelpuf", media=url)
#     tweeted = True
#   except twitter.error.TwitterError as err:
#     print("Tweet failed with error: {}".format(err))

# print("Tweet successful")

print("Process Complete")
