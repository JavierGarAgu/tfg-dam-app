from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('registros/', views.registros_view, name='registros'),
    path('logout/', views.logout_view, name='logout'),
    # Otras URLs que tengas definidas
]
