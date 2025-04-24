from django import forms
from .models import Flashcard, BoxLabel


class FlashcardForm(forms.ModelForm):
    delete_image = forms.BooleanField(required=False, label="Delete current image")
    delete_audio = forms.BooleanField(required=False, label="Delete current audio")

    class Meta:
        model = Flashcard
        fields = [
            "term",
            "definition",
            "category",
            "box",
            "image",
            "audio",  # ✅ Include audio
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].widget.clear_checkbox_label = ""
        if "audio" in self.fields:
            self.fields["audio"].widget.clear_checkbox_label = ""


class BoxLabelForm(forms.ModelForm):
    class Meta:
        model = BoxLabel
        fields = ["box_number", "label"]
