from django.contrib import admin
from django.urls import path
from .views import NewsView, PostView, NewsFilter

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', NewsView.as_view(), name='news'),

    #path('news/', PostsList.as_view(), name='news'),
    #path('', PostsList.as_view()), не удалил на случай изменений в будущем
    path('<int:pk>', PostView.as_view(), name='post_detail'),
    path('search/', NewsFilter.as_view(), name='post_filter'),
    #path('create/', PostCreate.as_view(), name='post_create'),
    #path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    #path('<int:pk>/create/', PostUpdate.as_view(), name='post_update'),
    #path('', IndexView.as_view()),
    #path('upgrade/', upgrade_me, name='upgrade'),
    #path('subscriptions/', subscribe, name='subscriptions'),
]
