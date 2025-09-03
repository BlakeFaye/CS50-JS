from django.urls import path

from . import views

handler404 = 'encyclopedia.views.custom_404_view'

urlpatterns = [
    path("", views.index, name="index"),
    path("CSS", views.CSS, name="CSS"),
    path("wiki", views.wiki, name="wiki"),
    path("wiki/<str:title>/", views.content, name="content"),
    path("search_result", views.search_result, name="search_result"),
    path("new_page", views.new_page, name="new_page"),
]

