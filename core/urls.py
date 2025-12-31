from django.contrib import admin
from django.urls import path, include
from core.views import *
from events.views import group_delete
from django.contrib.auth.views import PasswordChangeDoneView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('login/',log_in,name='login'),
    path('signup/',signup, name='signup'),
    path('logout/', log_out, name='logout'),
    path('admin/<int:user_id>/assign-role/',assign_role,name='assign-role'),
    path('admin/create-group/',create_group,name='create-group'),

    path('events/<int:event_id>/participants/', event_participants, name='event_participants'),
    path('participants/<int:id>/remove/', remove_participant, name='remove_participant'),
    path("activate/<int:user_id>/<str:token>/",activate_user),
    path('participant/home/', participant_home, name='paticipant_home'),
    path('events/<int:event_id>/rsvp/', rsvp_event, name='rsvp_event'),
    path('participant/my-rsvp/', my_rsvps, name='paticipant_dashboard'),
    path('participant/event_list/',event_list,name='p-event-list'),
    path('participant/<int:id>/event_details/',event_detail,name='p-event-details'),
    path('participant/search/',event_search,name='p-event-search'),
    

    path('organizer/search/',org_event_search,name='org-event-search'),
    path('organizer/<int:id>/event_details/',org_event_detail,name='org-event-details'),
    path('organizer/home/', orgHome, name='organizer-home'),
    path('organizer/categories/',category_list, name='category-list'),
    path('organizer/categories/create/',category_create, name='category-create'),
    path('organizer/categories/<int:id>/edit/',category_edit, name='category-edit'),
    path('organizer/categories/<int:id>/delete/',category_delete, name='category-delete'),
    
    path('organizer/events/', org_event_list, name='org-event-list'),
    path('organizer/dashboard/', org_dashboard, name='org-dashboard'),
    path('organizer/events/create/', eventcreate, name='org-event-create'),
    path('organizer/events/<int:id>/',eventdetails, name='org-event_detail'),
    path('organizer/events/<int:id>/view/', viewEvent, name='org-view-event'),
    path('organizer/events/<int:id>/edit/',eventupdate, name='org-event-update'),
    path('organizer/events/<int:id>/delete/', eventdelete, name='org-event-delete'),
    path('profile/',ProfileDetailView.as_view(),name='profile'),
    path('profile/update/',ProfileUpdateView.as_view(),name='profile_update'),
    path('password-change/',CustomPasswordChangeView.as_view(),name='change_password'),
    path('password-change/done/',CustomPasswordChangeDoneView.as_view(),name='password_change_done'),
    path('password-reset/',CustomPasswordResetView.as_view(),name='reset_password'),
    path('password-reset/confirm/<uidb64>/<token>/',CustomPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
