from django.urls import path
from . import views

urlpatterns = [
    path("", views.flashcard_list, name="flashcard_list"),
    path("edit/<int:pk>/", views.edit_flashcard, name="edit_flashcard"),
    path("promote/<int:card_id>/", views.promote_card, name="promote_card"),
    path("demote/<int:card_id>/", views.demote_card, name="demote_card"),
    path("box/<int:box_number>/", views.box_view, name="box_view"),
    path("create/", views.create_flashcard, name="create_flashcard"),
    path("edit/<int:card_id>/", views.edit_flashcard, name="edit_flashcard"),
    path("edit-box/<int:box_number>/", views.edit_box_label, name="edit_box_label"),
]
