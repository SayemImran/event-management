from django.urls import path, include
from events.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homepage, name='home'),
    path('events/', event_list, name='event_list'),
    path('events/create/', event_create, name='event_create'),
    path('events/<int:id>/', event_detail, name='event_detail'),
    path('events/<int:id>/view/', viewEvent, name='view-event'),
    path('events/<int:id>/edit/',event_update, name='event-update'),
    path('events/<int:event_id>/rsvp/', rsvp_event, name='rsvp_event'),
    path('events/<int:id>/delete/', event_delete, name='event_delete'),
    path('search/',event_search, name='event_search'),

    path('categories/',category_list, name='category_list'),
    path('categories/create/',category_create, name='category_create'),
    path('categories/<int:id>/edit/',category_edit, name='category_edit'),
    path('categories/<int:id>/delete/',category_delete, name='category_delete'),

    path('dashboard/', dashboard, name='dashboard'),
    path('groups/', showGroup, name='showgroup'),
    path('groups/delete/<int:id>/', group_delete, name='delete-group'),
  
    path('dashboard/pastevent/', pastEvent, name='past-event'),
    path('dashboard/upcomingevent/', upcommingEvent, name='up-event'),
    path('dashboard/totalevent/', totalEvent, name='total-event'),
    path('participants/', participant_list, name='participant_list')
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)