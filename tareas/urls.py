from django.urls import path

from . import views

urlpatterns = [
    path("", views.lista, name="lista"),
    path("editar/<int:pk>/", views.editar, name="editar"),
    path("completar/<int:pk>/", views.completar, name="completar"),
    path("eliminar/<int:pk>/", views.eliminar, name="eliminar"),
    path("salud/", views.salud, name="salud"),
]
