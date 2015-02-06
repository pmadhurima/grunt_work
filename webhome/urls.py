from django.conf.urls import url, patterns

from webhome import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^advice/$', views.advice, name='advice'),
    url(r'^contact/$',views.contact,name='contact'),
    url(r'^test/$',views.test, name='test'),
    url(r'^unknown',views.demo, name='unknown')
)