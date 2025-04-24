from django.db import models


class Flashcard(models.Model):
    term = models.CharField(max_length=100)
    definition = models.TextField()
    category = models.CharField(
        max_length=100, blank=True
    )  # e.g., Prefix, Root, Suffix
    box = models.IntegerField(default=1)  # 1 = New, 5 = Mastered
    image = models.ImageField(
        upload_to="card_images/", blank=True, null=True
    )  # ✅ Correct field
    audio = models.FileField(
        upload_to="card_audio/", blank=True, null=True
    )  # ✅ NEW FIELD

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.term


class BoxLabel(models.Model):
    box_number = models.IntegerField(unique=True)
    label = models.CharField(max_length=100, default="")

    def __str__(self):
        return f"Box {self.box_number}: {self.label}"
