from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cageInventory.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashdata/$','cageInventory.views.dashdata'),
    url(r'^check_in_out/(?P<item_id>.+)/(?P<uid>\d+)/$','cageInventory.views.check_in_out'),
    url(r'^graphdata/','cageInventory.views.graph_data'),
    url(r'^transaction/(?P<item_id>\d+)/$','cageInventory.views.transaction_detail'),
    url(r'^item/(?P<item_id>\d+)/$','cageInventory.views.item_detail'),
    url(r'^student/(?P<item_id>\d+)/$','cageInventory.views.student_detail'),
    url(r'^all/$','cageInventory.views.all_view'),
    url(r'^in/$','cageInventory.views.in_view'),
    url(r'^out/$','cageInventory.views.out_view'),
    url(r'^missing/$','cageInventory.views.missing_view'),
    url(r'^transactions/$','cageInventory.views.transactions_view'),
    url(r'^students/$','cageInventory.views.students'),
    url(r'^$', 'cageInventory.views.index'),
) 