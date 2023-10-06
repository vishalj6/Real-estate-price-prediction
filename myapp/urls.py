from django.urls import path
from . import views

urlpatterns = [
    path('', views.card, name='home'),
    path('chart1/', views.chart1_view, name='chart1'),
    path('chart2/', views.chart2_view, name='chart2'),
    path('chart3/', views.chart3_view, name='chart3'),
    path('details/', views.details, name='details'),
    path('card/', views.card, name='card'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='logout'),
    path('search/', views.search, name='search'),
    path('signup/', views.signup, name='signup'),
    path('predict/', views.predict_price, name='predict'),
    path('data/', views.data, name='data'),
    # path('import_csv/', views.import_csv, name='import_csv'),
]