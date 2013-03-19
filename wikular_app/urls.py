from django.conf.urls import patterns, url

from wikular_app import views

urlpatterns = patterns('', 
  url(r'^$', views.index, name='index'),
  url(r'^_cmd$', views.cmd, name='cmd'),
  url(r'^(?P<string_id>[a-zA-Z\d]{2,10})$', views.index, name='index'),
)




