# Generated by Django 3.2.13 on 2023-02-18 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='loggerDB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('bottleID', models.CharField(max_length=150)),
            ],
            options={
                'db_table': 'loggerDB',
            },
        ),
    ]
