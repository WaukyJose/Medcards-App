# Generated by Django 5.2 on 2025-04-24 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0003_boxlabel'),
    ]

    operations = [
        migrations.AddField(
            model_name='flashcard',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='flashcard_images/'),
        ),
    ]
