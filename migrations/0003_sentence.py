# Generated by Django 3.0.4 on 2021-10-13 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('english', '0002_words_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence', models.CharField(max_length=100)),
            ],
        ),
    ]
