from django.conf.urls import url

from . import views

app_name = 'game'
urlpatterns = [

    url(r'^add', views.add_name, name='add'),
    url(r'^delete/(?P<name>[A-Za-z0-9_-]*$)', views.delete_name, name='delete'),
    url(r'^all', views.get_all, name='all'),
    url(r'^lottery', views.lottery, name='lottery')
]