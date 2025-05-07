from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registros/', views.registros_view, name='registros'),
    path('registro/', views.registro_view, name='registro'),  # Nueva ruta para el registro
]

