# Generated by Django 2.2.5 on 2019-11-24 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capacityWeb', '0002_auto_20191122_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wifiinfo',
            fields=[
                ('tvid', models.IntegerField(db_column='tvId', primary_key=True, serialize=False)),
                ('sciencid', models.IntegerField(blank=True, db_column='sciencId', null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('adminid', models.CharField(blank=True, db_column='adminId', max_length=255, null=True)),
                ('adminname', models.CharField(blank=True, db_column='adminName', max_length=255, null=True)),
            ],
            options={
                'db_table': 'wifiinfo',
                'managed': False,
            },
        ),
    ]