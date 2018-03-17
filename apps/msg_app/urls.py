from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'users/show/(?P<number>[0-9]{1,})$', views.show, name="show"),
    url(r'process_message$', views.process_message, name="process_message"),
    url(r'process_comment$', views.process_comment, name="process_comment")
]