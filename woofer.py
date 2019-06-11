import os
import json
import random
import twitter
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials

c_key = os.environ["TWITTER_CONSUMER_KEY"]
c_secret = os.environ["TWITTER_CONSUMER_SECRET"]
a_token_key = os.environ["TWITTER_ACCESS_KEY"]
a_token_secret = os.environ["TWITTER_ACCESS_SECRET"]

api = twitter.Api(c_key, c_secret, a_token_key, a_token_secret)

image_index = int(os.environ["IMAGE_INDEX"])

if (os.path.getsize("image_file.txt") == 0):

  print("FETCHING NEW URLS")
  client = ImageSearchAPI(CognitiveServicesCredentials(os.environ["BING_KEY"]))

  image_results = []
  image_urls = []
  image_results.extend(client.images.search(query="cute dog").value)
  image_results.extend(client.images.search(query="puppies").value)

  for image in image_results:
    image_urls.append(image.content_url)

  with open('image_file.txt', 'a') as image_file:
    image_file.write(json.dumps(image_urls))

url_list = []
with open('image_file.txt', 'r') as image_file:
  url_list = json.load(image_file)

if (image_index > len(url_list)):
  image_index = 0

tweeted = False

while not tweeted:
  try:
    url = url_list[image_index]
    image_index += 1
    print("Attempting tweet of image url: {}".format(url))
    api.PostUpdate(". @CarterAlzamora @Houghelpuf", media=url)
    tweeted = True
  except twitter.error.TwitterError as err:
    print("Tweet failed with error: {}".format(err))

print("Tweet successful")

os.environ["IMAGE_INDEX"] = str(image_index)

print("Process Complete")
