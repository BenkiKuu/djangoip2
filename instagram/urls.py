from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from . import views

urlpatterns=[
    url('^$', views.news_today,name = 'newsToday'),
    url(r'^archives/(\d{4}-\d{2}-\d{2})/$',views.past_days_news,name = 'pastNews'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'^article/(?P<article_id>\d+)',views.article,name ='article'),
    url(r'^news/article/$', views.new_article, name='new_article'),
    url(r'^ajax/newsletter/$', views.newsletter, name='newsletter'),
    url(r'^profile/(?P<user_id>\d+)?', views.profile, name='profile'),
    url(r'^new-profile/', views.new_profile, name='new-profile'),


    # url(r'^api/merch/$', views.MerchList.as_view())
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
