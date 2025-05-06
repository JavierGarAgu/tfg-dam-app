from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registros/', views.registros_view, name='registros'),
    # Ruta para cerrar sesión
    path('logout/', views.logout_view, name='logout'),
]
