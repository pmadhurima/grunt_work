from django.conf.urls import include, url, patterns
from django.contrib import admin
from webhome.views import contact

urlpatterns = [
    # Examples:
    # url(r'^$', 'django_work.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^webhome/',include('webhome.urls')),
    url(r'^webhome/',contact)
]