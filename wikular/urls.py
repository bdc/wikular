from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wikular.views.home', name='home'),
    # url(r'^wikular/', include('wikular.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^wikular_app/', include('wikular_app.urls')),
    url(r'^$', include('wikular_app.urls')),
    url(r'^(?P<path>.*\.(?:jpg|css|png|js))$', 'django.views.static.serve', {
      'document_root' : settings.STATIC_ROOT,
    }),
)
