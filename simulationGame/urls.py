from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('configuration/', views.configuration, name='configuration'),
    path('round/<int:round_number>/<str:market>/', views.round_view, name='round_view'),
    path('results/<int:round_number>', views.results_view, name='results'),
    path('test/', views.test, name='test'),
    path('winner/', views.winner_view, name='show_winner'),
#    path('draw/', views.draw_view, name='draw'),
    path('instructions/', views.instructions_view, name='instractions'),
    #'results/<int:suppliers_number_A>/<int:suppliers_number_B>/<int:buyers_number_A>/<int:buyers_number_B>/'
]