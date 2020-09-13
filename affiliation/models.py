from django.db import models
from topic.models import Topics

# Create your models here.
class Affiliations(models.Model):
    id_univ = models.CharField(max_length=25,primary_key=True,db_column="id_univ")
    name = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    topik_dominan1 = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="topik_dominan1",to_field='id_topic',related_name="topik_dominan1_affi")
    nilai_dominan1 = models.IntegerField()
    topik_dominan2 = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="topik_dominan2",to_field='id_topic',related_name="topik_dominan2_affi")
    nilai_dominan2 = models.IntegerField()
    topik_dominan3 = models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="topik_dominan3",to_field='id_topic',related_name="topik_dominan3_affi")
    nilai_dominan3 = models.IntegerField()
    total_publication = models.IntegerField()
    total_cite = models.IntegerField()
    total_author = models.IntegerField()
    initial_univ = models.CharField(max_length=20)
    class Meta:
        db_table = "university"

class Data_sumcount_univ(models.Model):
    id = models.CharField(max_length=25, primary_key=True)
    univ = models.ForeignKey(Affiliations, on_delete=models.CASCADE,db_column="id_univ",to_field='id_univ',related_name="univ_sumcount")
    topic =models.ForeignKey(Topics, on_delete=models.CASCADE,db_column="id_topic",to_field='id_topic',related_name="topik_univ_sumcount")
    year = models.CharField(max_length=25)
    pubcount = models.CharField(max_length=25)
    sumcite = models.CharField(max_length=25)
    id_pub = models.CharField(max_length=25)
    class Meta:
        db_table = "data_sum_count_univ" 