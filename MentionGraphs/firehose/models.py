# encoding: utf-8

from django.db import models


class Keyword(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Metric(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255, null=True)

    def __unicode__(self):
        return "%s:%s" % (self.name, self.value)


class Datapoint(models.Model):
    keyword = models.ForeignKey(Keyword)
    time = models.DateTimeField()
    metric = models.ForeignKey(Metric, null=True)
    count = models.IntegerField()

    def __unicode__(self):
        return u"%s, %s, %s « %d »" % (self.keyword, self.time,
                                   self.metric, self.count)

def save_data(keyword, data):
    k = Keyword.objects.get_or_create(name=keyword)[0]
    for when, bucket in data.iteritems():
        for metric, count in bucket.iteritems():
            if metric is None:
                m = None
            else:
                (m_name, m_value) = metric
                m = Metric.objects.get_or_create(name=m_name, value=m_value)[0]
            Datapoint.objects.filter(keyword=k, metric=m, time=when).delete()
            dp = Datapoint(keyword=k, metric=m, time=when, count=count)
            dp.save()
