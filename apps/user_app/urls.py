from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index, name="index"), 
    #url(r'users$', views.index, name="index"), 
    url(r'edit$', views.edit, name="edit"), 
    url(r'edit/(?P<number>[0-9]{1,})$', views.edit_admin, name="edit_admin"), 
    url(r'update_my_info/(?P<number>[0-9]{1,})$', views.update_my_info, name="update_my_info"), 
    url(r'update_my_description/(?P<number>[0-9]{1,})$', views.update_my_description, name="update_my_description"),
    url(r'update_my_password/(?P<number>[0-9]{1,})$', views.update_my_password, name="update_my_password"),
    #url(r'users/show/(?P<number>[0-9]{1,})$', views.show, name="show"), #this is in msg_app...
    url(r'register$', views.register, name="register"), 
    url(r'users/new$', views.new, name="new"), 
    url(r'create$', views.create, name="create"), 
    url(r'signin$', views.sign_in, name="sign_in"), 
    url(r'verify$', views.verify_sign_in, name="verify_sign_in"), 
    url(r'logout$', views.log_out, name="log_out"),
    url(r'delete/(?P<number>[0-9]{1,})$', views.delete, name="delete"),
    url(r'dashboard$', views.dashboard, name="dashboard"), 
    url(r'dashboard/admin$', views.dashboard_admin, name="dashboard_admin")
]