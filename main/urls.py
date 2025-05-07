from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.main, name='main_page'),
    path('saved/', views.show_saved, name='saved_page'),
    path('swipe/', views.swipe_meme, name='swipe'),
    path('save/', views.save_meme, name='save'),
    path('matches/', views.show_matches, name='matches_page')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)