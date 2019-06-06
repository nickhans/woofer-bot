import os
import random
import twitter
from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials

client = ImageSearchAPI(CognitiveServicesCredentials(os.environ["BING_KEY"]))

c_key = os.environ["TWITTER_CONSUMER_KEY"]
c_secret = os.environ["TWITTER_CONSUMER_SECRET"]
a_token_key = os.environ["TWITTER_ACCESS_KEY"]
a_token_secret = os.environ["TWITTER_ACCESS_SECRET"]

api = twitter.Api(c_key, c_secret, a_token_key, a_token_secret)

image_results = client.images.search(query="cute dog")

if image_results.value:
  print("Length of results: {}".format(len(image_results.value)))
  random_img_index = random.randint(0, len(image_results.value) - 1)
  random_img_url = image_results.value[random_img_index].content_url
  print("Image at index {}: {}".format(random_img_index, random_img_url))
  api.PostUpdate(". @CarterAlzamora", media=random_img_url)
