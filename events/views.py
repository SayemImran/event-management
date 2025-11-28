from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from datetime import date
from events.models import Events, Participant, Category
from events.forms import EventForm, CategoryForm, ParticipantForm


from django.db.models import Q

def homepage(request):
    return render(request,"home.html")

def event_search(request):
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    results = Events.objects.select_related('category').prefetch_related('participants').all()

    # Text Search
    if query:
        results = results.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query)
        )

    # Category filter
    if category:
        results = results.filter(category_id=category)

    # Date range filter
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



def event_list(request):
    events = Events.objects.select_related("category").prefetch_related("participants")
    
    events = events.annotate(num_participants=Count("participants"))

    categories = Category.objects.all()

    return render(request, "event_list.html", {
        "events": events,
        "categories": categories,
    })

def viewEvent(request,id):
    event = get_object_or_404(Events, id=id)
    return render(request, "event_detail.html", {"event": event})

# event details
def event_detail(request, id):
    event = get_object_or_404(Events.objects.select_related("category").prefetch_related("participants"),id = id)
    return render(request, "event_detail.html", {"event": event})


#  create event
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("event_list")
    else:
        form = EventForm()

    return render(request, "event_form.html", {"form": form})


#  update event data
def event_update(request, id):
    event = get_object_or_404(Events, id=id)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("event_detail", id = id)
    else:
        form = EventForm(instance=event)

    return render(request, "event_form.html", {"form": form})

#  delete event
def event_delete(request, id):
    event = get_object_or_404(Events, id = id)

    if request.method == "POST":
        event.delete()
        return redirect("event_list")
    
    return render(request, "confirm_delete.html", {"obj": event})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

# Create category
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
def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'confirm_delete.html', {'obj': category})



'''
    participant part
'''
def participant_list(request):
    participants = Participant.objects.prefetch_related("event")
    return render(request,"participant_list.html",{"participants":participants})

def participant_create(request):
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("participant_list")
    else:
        form = ParticipantForm()
    return render(request, "participant_form.html", {"form": form, "title": "Add Participant"})


# Edit Participant
def participant_edit(request, id):
    participant = get_object_or_404(Participant, id=id)
    if request.method == "POST":
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect("participant_list")
    else:
        form = ParticipantForm(instance=participant)
    return render(request, "participant_form.html", {"form": form, "title": "Edit Participant"})


# Delete Participant
def participant_delete(request, id):
    participant = get_object_or_404(Participant, id=id)
    if request.method == "POST":
        participant.delete()
        return redirect("participant_list")
    return render(request, "confirm_delete.html", {"obj": participant})




def dashboard(request):
    events = Events.objects.select_related("category").prefetch_related("participants")
    categories = Category.objects.all()
    today = date.today()
    events = Events.objects.filter(start_date__lte=today, end_date__gte=today)
    totalevents = Events.objects.all()
    pastevents = Events.objects.filter(end_date__lt=today)
    upevents = Events.objects.filter(start_date__gt=today)
    all_participants = Participant.objects.all()
    context = {
        "totalevents":totalevents,
        "pastevents":pastevents,
        "upevents":upevents,
        "events":events,
        "categories" : categories,
        "all_participants":all_participants
    }
    return render(request,"dashboard.html",context)
    
def pastEvent(request):
    all_participants = Participant.objects.all()
    today = date.today()
    totalevents = Events.objects.all()
    pastevents = Events.objects.filter(end_date__lt=today)
    upevents = Events.objects.filter(start_date__gt=today)

    context = {
        "totalevents":totalevents,
        "pastevents":pastevents,
        "upevents":upevents,
        "all_participants":all_participants
    }
    return render(request, "pastEvent.html", context)
def upcommingEvent(request):
     all_participants = Participant.objects.all()
     today = date.today()
     totalevents = Events.objects.all()
     pastevents = Events.objects.filter(end_date__lt=today)
     upevents = Events.objects.filter(start_date__gt=today)

     context = {
        "totalevents":totalevents,
        "pastevents":pastevents,
        "upevents":upevents,
        "all_participants":all_participants
     }
     return render(request, "upcomingEvent.html", context)
def totalEvent(request):
     all_participants = Participant.objects.all()
     today = date.today()
     totalevents = Events.objects.all()
     pastevents = Events.objects.filter(end_date__lt=today)
     upevents = Events.objects.filter(start_date__gt=today)

     context = {
        "totalevents":totalevents,
        "pastevents":pastevents,
        "upevents":upevents,
        "all_participants":all_participants
     }
     return render(request,"totalEvent.html",context)