from django.db import models

# Create your models here.
class Topics(models.Model):
    id_topic = models.CharField(max_length=20, primary_key=True)
    topic_name = models.CharField(max_length=200)
    total_author = models.IntegerField()
    total_cite = models.IntegerField()
    total_publication = models.IntegerField()
    class Meta:
        db_table = "topic"

class Subtopics(models.Model):
    id_SubTopic = models.CharField(max_length=25, primary_key=True)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="id_topic",to_field='id_topic',related_name="topik_subtopik")
    no_subTopic = models.CharField(max_length=20)
    subtopic_name = models.CharField(max_length=255)

    class Meta:
        db_table = "subtopic"

class Svg_sub(models.Model):
    id = models.CharField(max_length=25, primary_key=True)
    # id_topic = models.CharField(max_length=25)
    subtopic = models.ForeignKey(Subtopics, on_delete=models.CASCADE,db_column="id_SubTopic",related_name="svg_sub",to_field='id_SubTopic')
    Year = models.CharField(max_length=25)
    kumAtas = models.CharField(max_length=25)
    kumBawah = models.CharField(max_length=25)
    batasAtas = models.CharField(max_length=25)
    batasBawah = models.CharField(max_length=25)
    class Meta:
        db_table = "svg_sub"   

class Data_sumcount_topic(models.Model):
    id = models.CharField(max_length=25, primary_key=True)
    topic =models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="id_topic",to_field='id_topic',related_name="topik_sumcount")
    year = models.CharField(max_length=25)
    pubcount = models.CharField(max_length=25)
    sumcite = models.CharField(max_length=25)
    id_univ = models.CharField(max_length=20)
    class Meta:
        db_table = "data_sum_count_topic" 

class Dyna_prod(models.Model):
    id_dyna_prod = models.CharField(max_length=20, primary_key=True)
    nidn = models.CharField(max_length=25)
    id_topic = models.CharField(max_length=20)
    F2rep = models.FloatField()
    F3sum = models.FloatField()
    F4min = models.FloatField()
    F5end = models.FloatField()
    class Meta:
        db_table = "dyna_prod"