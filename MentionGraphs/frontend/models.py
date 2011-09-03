from django.db import models

metric_ids = {
    'lang-en': 1,
    'lang-de': 2,
    'sentiment-positive': 3,
    'sentiment-neutral': 4,
    'sentiment-negative': 5,
}

class Datapoint(models.Model):
    time = models.IntegerField()
    metric = models.IntegerField()
    value = models.IntegerField()
