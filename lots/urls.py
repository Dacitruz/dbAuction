from django.urls import path, re_path
from .views import index, check, create, edit, remove, all_lots, bid_lots


urlpatterns = [
    path('', index),
    path('index', index),
    path('create', create),
    path('all_lots', all_lots),
    path('my_bids', bid_lots),
    re_path(r'^check/(?P<post_id>[0-9]+)$', check),
    re_path(r'^edit/(?P<post_id>[0-9]+)$', edit),
    re_path(r'^remove/(?P<post_id>[0-9]+)$', remove),

]