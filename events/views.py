from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from datetime import date
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User, Group, Permission
from events.models import Events, Category,RSVP
from events.forms import EventForm, CategoryForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
def homepage(request):
    return render(request,"home.html")

def only_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_admin(user):
    return user.groups.filter(name='Organizers').exists() or user.groups.filter(name='Admin').exists()
@login_required
def event_search(request):
    if not request.user.groups.filter(name='Organizers').exists():
        return render(request, "no_permission.html")  
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    results = Events.objects.select_related('category').prefetch_related('rsvps')

    if query:
        results = results.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query)
        )

    if category:
        results = results.filter(category_id=category)

    if start_date and end_date:
        results = results.filter(
            Q(start_date__lte=end_date) &
            Q(end_date__gte=start_date)
        )

    categories = Category.objects.all()

    return render(request, 'event_search.html', {
        'results': results,
        'query': query,
        'categories': categories,
        'selected_category': category,
        'start': start_date,
        'end': end_date,
    })

@login_required
def event_list(request):
    events = Events.objects.select_related("category").prefetch_related("rsvps")
    events = events.annotate(num_participants=Count("rsvps"))

    categories = Category.objects.all()

    return render(request, "event_list.html", {
        "events": events,
        "categories": categories,
    })


def viewEvent(request,id):
    event = get_object_or_404(Events, id=id)
    return render(request, "event_detail.html", {"event": event})

# event details
@login_required
def event_detail(request, id):
    event = get_object_or_404(
        Events.objects.select_related("category").prefetch_related("rsvps"),
        id=id
    )

    try:
        user_rsvp = RSVP.objects.get(user=request.user, event=event)
    except RSVP.DoesNotExist:
        user_rsvp = None

    rsvp_participants = RSVP.objects.filter(event=event).select_related('user')

    context = {
        "event": event,
        "user_rsvp": user_rsvp,
        "rsvp_participants": rsvp_participants
    }

    return render(request, "event_detail.html", context)

@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Events, id=event_id)

    if request.method == "POST":
        status = request.POST.get('status')

        rsvp, created = RSVP.objects.get_or_create(
            user=request.user,
            event=event,
            defaults={'status': status}
        )

        if not created:
            print("Already invited")
            rsvp.status = status
            rsvp.save()

       
        if created and status == 'going':
            subject = f"RSVP Confirmation  {event.name}"
            message = (
                f"Hello {request.user.first_name},\n\n"
                f"You have successfully RSVP'd as GOING to:\n"
                f"{event.name}\n\n"
                f"Location: {event.location}\n"
                f"Date: {event.start_date}\n\n"
                f"Thank you! 💝"
            )
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False
            )

    return redirect('event_detail', id=event.id)

@login_required
def my_rsvps(request):
    rsvps = RSVP.objects.filter(user=request.user).select_related('event')
    return render(request, 'participant/dashboard.html', {'rsvps': rsvps})


#  create event
@login_required
@user_passes_test(is_admin)
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("event_list")
    else:
        form = EventForm()

    return render(request, "event_form.html", {"form": form})


#  update event data
@login_required
@user_passes_test(is_admin)
def event_update(request, id):
    event = get_object_or_404(Events, id=id)

    if request.method == "POST":
        form = EventForm(request.POST,request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event_detail", id = id)
    else:
        form = EventForm(instance=event)

    return render(request, "event_form.html", {"form": form})

#  delete event
@login_required
@user_passes_test(is_admin)
def event_delete(request, id):
    event = get_object_or_404(Events, id = id)

    if request.method == "POST":
        event.delete()
        return redirect("event_list")
    
    return render(request, "confirm_delete.html", {"obj": event})
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

# Create category
@login_required
@user_passes_test(is_admin)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form, 'title': 'Create Category'})

# Edit category
@login_required
@user_passes_test(is_admin)
def category_edit(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form, 'title': 'Edit Category'})

# Delete category
@login_required
@user_passes_test(is_admin)
def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'confirm_delete.html', {'obj': category})

@login_required
@user_passes_test(only_admin)
def dashboard(request):
    today = date.today()

    totalevents = Events.objects.all()
    pastevents = Events.objects.filter(end_date__lt=today)
    upevents = Events.objects.filter(start_date__gt=today)
    events = Events.objects.filter(start_date__lte=today, end_date__gte=today)

    categories = Category.objects.all()
    all_participants = User.objects.filter(groups__name='Participant')

    context = {
        "totalevents": totalevents,
        "pastevents": pastevents,
        "upevents": upevents,
        "events": events,
        "categories": categories,
        "all_participants": all_participants
    }
    return render(request, "dashboard.html", context)

@login_required
@user_passes_test(only_admin)
def pastEvent(request):
    today = date.today()

    totalevents = Events.objects.all()
    pastevents = Events.objects.filter(end_date__lt=today)
    upevents = Events.objects.filter(start_date__gt=today)

    all_participants = User.objects.filter(groups__name='Participant')

    context = {
        "totalevents": totalevents,
        "pastevents": pastevents,
        "upevents": upevents,
        "all_participants": all_participants
    }
    return render(request, "pastEvent.html", context)

@login_required
@user_passes_test(only_admin)
def upcommingEvent(request):
    today = date.today()

    totalevents = Events.objects.all()
    pastevents = Events.objects.filter(end_date__lt=today)
    upevents = Events.objects.filter(start_date__gt=today)

    all_participants = User.objects.filter(groups__name='Participant')

    context = {
        "totalevents": totalevents,
        "pastevents": pastevents,
        "upevents": upevents,
        "all_participants": all_participants
    }
    return render(request, "upcomingEvent.html", context)

@login_required
@user_passes_test(only_admin)
def totalEvent(request):
    today = date.today()

    totalevents = Events.objects.all()
    pastevents = Events.objects.filter(end_date__lt=today)
    upevents = Events.objects.filter(start_date__gt=today)

    all_participants = User.objects.filter(groups__name='Participant')

    context = {
        "totalevents": totalevents,
        "pastevents": pastevents,
        "upevents": upevents,
        "all_participants": all_participants
    }
    return render(request, "totalEvent.html", context)
@login_required
def participant_list(request):
    all_participants = User.objects.filter(groups__name='Participants')
    context = {
        'all_participants': all_participants
    }
    return render(request, "participant_list.html", context)

@login_required
@user_passes_test(only_admin)
def showGroup(request):
    groups = Group.objects.all()
    return render(request,'showGroup.html',{"groups":groups})
@login_required
@user_passes_test(only_admin)
def group_delete(request,id):
    group = get_object_or_404(Group, id=id)

    if request.method == "POST":
        group_name = group.name
        group.delete()
        messages.success(request, f"Group '{group_name}' has been deleted successfully.")
        return redirect('showgroup')

    return render(request, 'showGroup.html', {'obj': group})