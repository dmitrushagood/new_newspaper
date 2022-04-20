from django.urls import path
from .views import NewsView, PostView, NewsFilter, PostCreate, PostUpdate, PostDelete, upgrade_me, Upgraded

urlpatterns = [
    path('', NewsView.as_view(), name='news'),

    #path('news/', PostsList.as_view(), name='news'),
    #path('', PostsList.as_view()), не удалил на случай изменений в будущем
    path('<int:pk>', PostView.as_view(), name='post_detail'),
    path('search/', NewsFilter.as_view(), name='post_filter'),

    path('add/', PostCreate.as_view(), name='post_add'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('upgraded/', Upgraded.as_view(), name='upgraded'),
    #path('', IndexView.as_view()),
    #path('upgrade/', upgrade_me, name='upgrade'),
    #path('subscriptions/', subscribe, name='subscriptions'),
]
