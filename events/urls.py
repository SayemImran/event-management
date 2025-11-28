from django.urls import path, include
from events.views import *
urlpatterns = [
    path('', homepage, name='home'),
    path('events/', event_list, name='event_list'),
    path('events/create/', event_create, name='event_create'),
    path('events/<int:id>/', event_detail, name='event_detail'),
    path('events/<int:id>/view/', viewEvent, name='view-event'),
    path('events/<int:id>/edit/',event_update, name='event-update'),
    path('events/<int:id>/delete/', event_delete, name='event_delete'),
    path('search/',event_search, name='event_search'),

    path('categories/',category_list, name='category_list'),
    path('categories/create/',category_create, name='category_create'),
    path('categories/<int:id>/edit/',category_edit, name='category_edit'),
    path('categories/<int:id>/delete/',category_delete, name='category_delete'),

    path('participants/',participant_list, name='participant_list'),
    path('participants/create/', participant_create, name='participant_create'),
    path('participants/<int:id>/edit/', participant_edit, name='participant_edit'),
    path('participants/<int:id>/delete/', participant_delete, name='participant_delete'),

    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/pastevent/', pastEvent, name='past-event'),
    path('dashboard/upcomingevent/', upcommingEvent, name='up-event'),
    path('dashboard/totalevent/', totalEvent, name='total-event')
]