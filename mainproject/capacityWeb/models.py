from django.db import models


# Create your models here.

class Camera(models.Model):
    camid = models.CharField(db_column='camId', primary_key=True, max_length=11)  # Field name made lowercase.
    scenicid = models.ForeignKey('Scenic', models.DO_NOTHING, db_column='scenicId')  # Field name made lowercase.
    camplace = models.CharField(db_column='camPlace', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.
    camlng = models.FloatField(db_column='camLng', blank=True, null=True)  # Field name made lowercase.
    camlat = models.FloatField(db_column='camLat', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'camera'
        unique_together = (('camid', 'scenicid'),)


class Recordnums(models.Model):
    scenicid = models.ForeignKey('Scenic', models.DO_NOTHING, db_column='scenicId')  # Field name made lowercase.
    camid = models.ForeignKey(Camera, models.DO_NOTHING, db_column='camId', blank=True,
                              null=True)  # Field name made lowercase.
    nums = models.IntegerField(blank=True, null=True)
    year = models.IntegerField()
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    hour = models.IntegerField(blank=True, null=True)
    minute = models.IntegerField(blank=True, null=True)
    sec = models.IntegerField(blank=True, null=True)
    createat = models.CharField(db_column='createAt', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:

        db_table = 'recordnums'


class Recordwarnings(models.Model):
    warningid = models.AutoField(db_column='warningId', primary_key=True)  # Field name made lowercase.
    scenicid = models.CharField(db_column='scenicId', max_length=11, blank=True,
                                null=True)  # Field name made lowercase.
    camid = models.CharField(db_column='camId', max_length=11, blank=True, null=True)  # Field name made lowercase.
    level = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    createat = models.CharField(db_column='createAt', max_length=255, blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'recordwarnings'


class Scenic(models.Model):
    scenicid = models.CharField(db_column='scenicId', primary_key=True, max_length=11)  # Field name made lowercase.
    scenicname = models.CharField(db_column='scenicName', max_length=255, blank=True,
                                  null=True)  # Field name made lowercase.
    warning1nums = models.IntegerField(db_column='warning1Nums', blank=True, null=True)  # Field name made lowercase.
    warning2nums = models.IntegerField(db_column='warning2Nums', blank=True, null=True)  # Field name made lowercase.
    warning3nums = models.IntegerField(db_column='warning3Nums', blank=True, null=True)  # Field name made lowercase.
    lng = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scenic'
