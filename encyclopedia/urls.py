from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki", views.index, name="index"),
    path("wiki/<str:name>", views.search, name="search"),
    path("searchEntry", views.searchEntry, name="searchEntry"),
    path("newEntryPage", views.newEntryPage, name="newEntryPage"),
    path("newEntry", views.newEntry, name="newEntry"),
    path(r'^editPage/(?P<entry>/w+)/$', views.editPage, name="editPage"),
    path('randomPage', views.randomPage, name="randomPage")
]
