from django.conf.urls import url
from views import index,show_create,show_dashboard,show_main,create,view_item,add_product_to_mylist,remove_product_from_mylist
from ..login_reg_app.views import login, register, success, logout


urlpatterns = [
    url(r'^$', index),
    url(r'^main$', show_main),
    url(r'^login$', login),
    url(r'^register$', register),
    url(r'^success$', success),
    url(r'^logout$', logout),
    url(r'^dashboard$', show_dashboard),
    url(r'^wish_item/create$', show_create),
    url(r'^create$', create),
    url(r'^wish_items/(?P<id>\d+)$', view_item),
    url(r'^addtomylist/(?P<id>\d+)/(?P<username>\w+)$', add_product_to_mylist),
    url(r'^remove/(?P<id>\d+)$', remove_product_from_mylist)
]
