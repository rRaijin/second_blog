from django.conf.urls import url
from blog import views


urlpatterns = [

    # url(r'^create/$', views.post_create, name='create'),
    url(r'^$', views.post_list, name='list'),
    url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete, name='delete'),
    url(r'^(?P<slug>[\w-]+)/like/$', views.add_likes, name='like'),
    url(r'^(?P<slug>[\w-]+)/dislike/$', views.add_dislike, name='dislike'),
    url(r'^(?P<slug>[\w-]+)/addcomment/$', views.add_comment, name='add_comment'),
    url(r'^category/(?P<category_name>[-\w]+)/$', views.category, name='category'),
    url(r'^category/(?P<category_name>[-\w]+)/create/$', views.post_create, name='create'),

]
