from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('registros/', views.registros_view, name='registros'),
    path('eliminar_registro/<int:id>/', views.eliminar_registro, name='eliminar_registro'),
    path('actualizar_registro/', views.actualizar_registro, name='actualizar_registro'),
    path('nuevo_registro/', views.nuevo_registro, name='nuevo_registro'),
    path('info_coche/', views.info_coche, name='info_coche'),
]

