from django.urls import path
from encyclopedia.views import fourofour

from . import views

handler404 = fourofour

urlpatterns = [
    path("", views.index, name="index"),
    path("CSS", views.CSS, name="CSS"),
    path("wiki", views.wiki, name="wiki"),
    path("wiki/<str:title>/", views.content, name="content"),
    path("fourofour", views.fourofour, name="fourofour"),
]

