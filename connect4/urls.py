from django.conf.urls import url
import django.contrib.auth
import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    url(
        r'^login/$',
        views.login
    ),
    url(
        r'^logout/$',
        views.logout
    ),
    url(
        r'^signup/$',
        views.signup
    ),
    url(r'^games/$', views.games),
    url(r'^play/$', views.play),
    url(r'^play/(?P<game_id>\d+)/$', views.play)
]
