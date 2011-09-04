from django.db import models


class Keyword(models.Model):
    name = models.CharField(max_length=255)


class Metric(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)


class Datapoint(models.Model):
    keyword = models.ForeignKey(Keyword)
    time = models.DateTimeField()
    metric = models.ForeignKey(Metric)
    count = models.IntegerField()

def save_data(keyword, data):
    k = Keyword.objects.get_or_create(name=keyword)[0]
    for when, bucket in data.iteritems():
        for (m_name, m_value), count in bucket.iteritems():
            m = Metric.objects.get_or_create(name=m_name, value=m_value)[0]
            dp = Datapoint(keyword=k, metric=m, time=when, count=count)
            dp.save()
