from django.shortcuts import render, get_object_or_404, redirect
from .models import Flashcard
from .forms import BoxLabelForm


def flashcard_list(request):
    boxes = [Flashcard.objects.filter(box=i) for i in range(1, 6)]
    all_count = Flashcard.objects.count()
    box_counts = [box.count() for box in boxes]
    return render(
        request,
        "flashcards/card_list.html",
        {
            "boxes": boxes,
            "all_count": all_count,
            "box_counts": box_counts,
        },
    )


def box_view(request, box_number):
    cards = Flashcard.objects.filter(box=box_number)

    if not cards.exists():
        return render(
            request,
            "flashcards/box_session.html",
            {"card": None, "box_number": box_number},
        )

    card = cards.order_by("?").first()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "promote":
            card.box = min(card.box + 1, 5)
        elif action == "demote":
            card.box = max(card.box - 1, 1)
        card.save()
        return redirect("box_view", box_number=box_number)

    return render(
        request,
        "flashcards/box_session.html",
        {"card": card, "box_number": box_number, "remaining": cards.count()},
    )


from .forms import FlashcardForm


def create_flashcard(request):
    if request.method == "POST":
        form = FlashcardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.box = 1
            card.save()
            generate_audio(card)  # TTS here
            card.save()
            return redirect("flashcard_list")
    else:
        form = FlashcardForm()
    return render(request, "flashcards/create_flashcard.html", {"form": form})


def promote_card(request, card_id):
    card = get_object_or_404(Flashcard, id=card_id)
    if card.box < 5:
        card.box += 1
        card.save()
    return redirect("flashcard_list")


def demote_card(request, card_id):
    card = get_object_or_404(Flashcard, id=card_id)
    card.box = 1
    card.save()
    return redirect("flashcard_list")


def edit_flashcard(request, pk):
    card = get_object_or_404(Flashcard, pk=pk)
    old_term = card.term  # save original term

    if request.method == "POST":
        form = FlashcardForm(request.POST, request.FILES, instance=card)
        if form.is_valid():
            if form.cleaned_data.get("delete_image") and card.image:
                card.image.delete(save=False)
                card.image = None
            if form.cleaned_data.get("delete_audio") and card.audio:
                card.audio.delete(save=False)
                card.audio = None

            form.save()

            if old_term != card.term:
                generate_audio(card)  # only regenerate if term changed

            card.save()
            return redirect("flashcard_list")
    else:
        form = FlashcardForm(instance=card)

    return render(request, "flashcards/edit_flashcard.html", {"form": form})


from .models import Flashcard, BoxLabel


def get_box_labels():
    labels = BoxLabel.objects.all()
    default_labels = ["1st Box", "2nd Box", "3rd Box", "4th Box", "5th Box"]
    box_labels = {}
    for i in range(1, 6):
        label_obj = labels.filter(box_number=i).first()
        box_labels[i] = label_obj.label if label_obj else default_labels[i - 1]
    return box_labels


def flashcard_list(request):
    boxes = [Flashcard.objects.filter(box=i) for i in range(1, 6)]
    box_labels = get_box_labels()
    return render(
        request,
        "flashcards/card_list.html",
        {
            "boxes": boxes,
            "all_count": Flashcard.objects.count(),
            "box_counts": [b.count() for b in boxes],
            "box_labels": box_labels,
        },
    )


def edit_box_label(request, box_number):
    label, _ = BoxLabel.objects.get_or_create(box_number=box_number)
    if request.method == "POST":
        form = BoxLabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            return redirect("flashcard_list")
    else:
        form = BoxLabelForm(instance=label)
    return render(
        request,
        "flashcards/edit_box_label.html",
        {"form": form, "box_number": box_number},
    )


from gtts import gTTS
import os
from django.core.files import File


def generate_audio(card):
    tts = gTTS(text=card.term, lang="en")
    audio_path = f"media/card_audio/{card.term}.mp3"
    tts.save(audio_path)
    with open(audio_path, "rb") as f:
        card.audio.save(f"{card.term}.mp3", File(f), save=False)
    os.remove(audio_path)
