import json
import random

from app.models import *

def run():
    with open("scripts/data/all_comments_with_sentiment.json") as jsonfile:
        data = json.load(jsonfile)

    negative_messages = list(filter(lambda x: (x['sentiment'] == "-1"), data))
    positive_messages = list(filter(lambda x: (x['sentiment'] == "1"), data))
    neutral_messages = list(filter(lambda x: (x['sentiment'] == "0"), data))

    sample_neg = random.sample(negative_messages, 350)
    sample_pos = random.sample(positive_messages, 350)
    sample_neu = random.sample(neutral_messages, 300)

    final_list = sample_pos + sample_neg + sample_neu

    for item in final_list:
        obj = Item(validation=Validation.objects.get(pk=1), payload=item)
        obj.save()
