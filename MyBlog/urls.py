from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()

urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('loginsys.urls')),
    url(r'^', include('blog.urls', namespace='posts')),
]\
                +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
                +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

