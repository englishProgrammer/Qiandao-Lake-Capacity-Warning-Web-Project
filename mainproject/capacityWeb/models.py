# registed
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Camera(models.Model):
    camid = models.CharField(db_column='camId', primary_key=True, max_length=11)  # Field name made lowercase.
    scenicid = models.ForeignKey('Scenic', models.DO_NOTHING, db_column='scenicId')  # Field name made lowercase.
    camplace = models.CharField(db_column='camPlace', max_length=255, blank=True, null=True)  # Field name made lowercase.
    camlng = models.FloatField(db_column='camLng', blank=True, null=True)  # Field name made lowercase.
    camlat = models.FloatField(db_column='camLat', blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(max_length=255, blank=True, null=True)
    adminid = models.CharField(db_column='adminId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adminname = models.CharField(db_column='adminName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    devicetype = models.CharField(db_column='deviceType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'camera'
        unique_together = (('camid', 'scenicid'),)


class Camerainfo(models.Model):
    cameraid = models.IntegerField(db_column='cameraId', primary_key=True)  # Field name made lowercase.
    sciencid = models.IntegerField(db_column='sciencId')  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    adminid = models.IntegerField(db_column='adminId', blank=True, null=True)  # Field name made lowercase.
    adminname = models.CharField(db_column='adminName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    devicetype = models.CharField(db_column='deviceType', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'camerainfo'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Mobile(models.Model):
    todaydividual = models.CharField(db_column='todayDividual', max_length=255, blank=True, null=True)  # Field name made lowercase.
    todayteam = models.CharField(db_column='todayTeam', max_length=255, blank=True, null=True)  # Field name made lowercase.
    todaytotal = models.CharField(db_column='todayTotal', max_length=255, blank=True, null=True)  # Field name made lowercase.
    centerdividual = models.CharField(db_column='centerDividual', max_length=255, blank=True, null=True)  # Field name made lowercase.
    centerteam = models.CharField(db_column='centerTeam', max_length=255, blank=True, null=True)  # Field name made lowercase.
    centerin = models.CharField(db_column='centerIn', max_length=255, blank=True, null=True)  # Field name made lowercase.
    eastsouthdividual = models.CharField(db_column='eastsouthDividual', max_length=255, blank=True, null=True)  # Field name made lowercase.
    eastsouthteam = models.CharField(db_column='eastsouthTeam', max_length=255, blank=True, null=True)  # Field name made lowercase.
    eastsouthin = models.CharField(db_column='eastSouthIn', max_length=255, blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(blank=True, null=True)
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    ticketdate = models.CharField(db_column='ticketDate', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'mobile'


class Recordnums(models.Model):
    scenicid = models.ForeignKey('Scenic', models.DO_NOTHING, db_column='scenicId')  # Field name made lowercase.
    camid = models.ForeignKey(Camera, models.DO_NOTHING, db_column='camId', blank=True, null=True)  # Field name made lowercase.
    nums = models.IntegerField(blank=True, null=True)
    year = models.IntegerField()
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    hour = models.IntegerField(blank=True, null=True)
    minute = models.IntegerField(blank=True, null=True)
    sec = models.IntegerField(blank=True, null=True)
    createat = models.CharField(db_column='createAt', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'recordnums'


class Recordwarnings(models.Model):
    warningid = models.AutoField(db_column='warningId', primary_key=True)  # Field name made lowercase.
    scenicid = models.CharField(db_column='scenicId', max_length=11, blank=True, null=True)  # Field name made lowercase.
    camid = models.CharField(db_column='camId', max_length=11, blank=True, null=True)  # Field name made lowercase.
    level = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    exceednums = models.IntegerField(db_column='exceedNums', blank=True, null=True)  # Field name made lowercase.
    createat = models.CharField(db_column='createAt', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'recordwarnings'


class Scenic(models.Model):
    scenicid = models.CharField(db_column='scenicId', primary_key=True, max_length=11)  # Field name made lowercase.
    scenicname = models.CharField(db_column='scenicName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    warning1nums = models.IntegerField(db_column='warning1Nums', blank=True, null=True)  # Field name made lowercase.
    warning2nums = models.IntegerField(db_column='warning2Nums', blank=True, null=True)  # Field name made lowercase.
    warning3nums = models.IntegerField(db_column='warning3Nums', blank=True, null=True)  # Field name made lowercase.
    lng = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'scenic'


class Wifi(models.Model):
    scenicid = models.CharField(db_column='scenicId', max_length=11, blank=True, null=True)  # Field name made lowercase.
    camid = models.CharField(db_column='camId', max_length=11, blank=True, null=True)  # Field name made lowercase.
    apcn = models.CharField(max_length=255, blank=True, null=True)
    stamac = models.CharField(db_column='staMac', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tertype = models.CharField(db_column='terType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vendorcn = models.CharField(db_column='vendorCn', max_length=255, blank=True, null=True)  # Field name made lowercase.
    starxbytes = models.CharField(db_column='staRxbytes', max_length=255, blank=True, null=True)  # Field name made lowercase.
    statxbytes = models.CharField(db_column='staTxbytes', max_length=255, blank=True, null=True)  # Field name made lowercase.
    year = models.CharField(max_length=255)
    month = models.CharField(max_length=255, blank=True, null=True)
    day = models.CharField(max_length=255, blank=True, null=True)
    hour = models.CharField(max_length=255, blank=True, null=True)
    minute = models.CharField(max_length=255, blank=True, null=True)
    createat = models.CharField(db_column='createAt', max_length=255, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(max_length=255, blank=True, null=True)
    adminid = models.CharField(db_column='adminId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adminname = models.CharField(db_column='adminName', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wifi'


class Wifiinfo(models.Model):
    devicetype = models.CharField(db_column='deviceType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tvid = models.IntegerField(db_column='tvId', primary_key=True)  # Field name made lowercase.
    sciencid = models.IntegerField(db_column='sciencId', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    adminid = models.CharField(db_column='adminId', max_length=255, blank=True, null=True)  # Field name made lowercase.
    adminname = models.CharField(db_column='adminName', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'wifiinfo'
