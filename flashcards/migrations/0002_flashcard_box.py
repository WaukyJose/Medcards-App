# Generated by Django 5.2 on 2025-04-19 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcard',
            name='box',
            field=models.IntegerField(default=1),
        ),
    ]
