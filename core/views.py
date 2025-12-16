from django.shortcuts import render,redirect
from django.http import HttpResponse
from core.forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User,Group,Permission
from django.shortcuts import render, get_object_or_404, redirect
from events.models import Events
from events.forms import *
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login,logout
from django.contrib import messages
from django.db.models import Count, Q
from datetime import date
from events.models import Events, Category,RSVP
from django.core.mail import send_mail
from django.conf import settings
from events.views import is_admin

def orgHome(request):
    return render(request,'organizer/organizer_home.html')
def signup(request):   
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            # messages.success(request,'A confirmation mail sent. Please check your email')
            return redirect("login")
    else:
        form = CustomRegistrationForm()
    return render(request,"signup.html",{"form":form})

def log_in(request):
    form = LoginForm()
    if request.method == "POST":
        form= LoginForm(data=request.POST)
        if form.is_valid():   
            user = form.get_user()
            login(request,user)
            
            if user.groups.filter(name='Participants').exists():    
                return redirect('paticipant_dashboard')
            elif user.groups.filter(name='Organizers').exists():
                return redirect('organizer-home')
            else:
                return redirect('home')
    return render(request,"login.html",{"form":form})

def log_out(request):
    if request.method=='POST':
        logout(request)
        return redirect('login')
    return redirect('login')
def activate_user(request, user_id, token):
   try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user,token):
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return HttpResponse("Invalid ID or Token")
   except User.DoesNotExist:
       return HttpResponse("User does not exists")

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()


def event_participants(request, event_id):
    event = get_object_or_404(Events, id=event_id)
    participants = event.participants.all()  # RSVP’d users
    context = {
        'event': event,
        'participants': participants
    }
    return render(request, "event_participants.html", context)


def remove_participant(request, id):
    user = get_object_or_404(User, id=id)
    if request.user == user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('participant_list')

    if request.method == "POST":
        username = user.username
        user.delete()
        messages.success(
            request,
            f"User '{username}' deleted successfully."
        )
        return redirect('participant_list')
    return redirect('participant_list')
    # return render(request,'participant_list.html')
    

def assign_role(request,user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method=='POST':
        form = AssignRoleForm(request.POST)
        
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()
            
            user.groups.add(role)
            return redirect('participant_list')
    return render(request,'assign_role.html',{"form":form})

def create_group(request):
    form = CreateGroupForm()
    
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        
        if form.is_valid():
            group = form.save()
            messages.success(request,f'Group {group.name} has been created successfully')
            return redirect('create-group')
    return render(request,'create_group.html',{"form":form})


def event_search(request):
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

    return render(request, 'participant/search_result.html', {
        'results': results,
        'query': query,
        'categories': categories,
        'selected_category': category,
        'start': start_date,
        'end': end_date,
    })

def org_event_search(request):
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

    return render(request, 'organizer/event_search.html', {
        'results': results,
        'query': query,
        'categories': categories,
        'selected_category': category,
        'start': start_date,
        'end': end_date,
    })


def event_list(request):
    events = Events.objects.select_related("category").prefetch_related("rsvps")
    events = events.annotate(num_participants=Count("rsvps"))

    categories = Category.objects.all()

    return render(request, "participant/participant_event.html", {
        "events": events,
        "categories": categories,
    })
    
def org_event_list(request):
    events = Events.objects.select_related("category").prefetch_related("rsvps")
    events = events.annotate(num_participants=Count("rsvps"))

    categories = Category.objects.all()

    return render(request, "organizer/event_list.html", {
        "events": events,
        "categories": categories,
    })

def org_dashboard(request):
    events = Events.objects.all()
    categories = Category.objects.all()
    return render(request,'organizer/dashboard.html',{"events":events,"categories":categories})
def viewEvent(request,id):
    event = get_object_or_404(Events, id=id)
    return render(request, "organizer/event_detail.html", {"event": event})

# event details
#
def event_detail(request, id):
    event = get_object_or_404(
        Events.objects.select_related("category").prefetch_related("rsvps"),
        id=id
    )

    try:
        user_rsvp = RSVP.objects.get(user=request.user, event=event)
    except RSVP.DoesNotExist:
        user_rsvp = None

    # RSVP participant list (with status)
    rsvp_participants = RSVP.objects.filter(event=event).select_related('user')

    context = {
        "event": event,
        "user_rsvp": user_rsvp,
        "rsvp_participants": rsvp_participants
    }

    return render(request, "participant/participant_event_detail.html", context)

#
#(is_admin)
def org_event_detail(request, id):
    event = get_object_or_404(
        Events.objects.select_related("category").prefetch_related("rsvps"),
        id=id
    )

    try:
        user_rsvp = RSVP.objects.get(user=request.user, event=event)
    except RSVP.DoesNotExist:
        user_rsvp = None

    # RSVP participant list (with status)
    rsvp_participants = RSVP.objects.filter(event=event).select_related('user')

    context = {
        "event": event,
        "user_rsvp": user_rsvp,
        "rsvp_participants": rsvp_participants
    }

    return render(request, "organizer/event_detail.html", context)


#
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

    return redirect('p-event-details', id=event.id)

#
def my_rsvps(request):
    rsvps = RSVP.objects.filter(user=request.user).select_related('event')
    return render(request, 'participant/dashboard.html', {'rsvps': rsvps})

def participant_home(request):
    return render(request,'participant/participant_home.html')


#  Organizers power
def eventcreate(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("org-event-list")
    else:
        form = EventForm()

    return render(request, "organizer/event_form.html", {"form": form})


#  update event data
#
#(is_admin)
def eventupdate(request, id):
    event = get_object_or_404(Events, id=id)

    if request.method == "POST":
        form = EventForm(request.POST,request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("org-event_detail", id = id)
    else:
        form = EventForm(instance=event)

    return render(request, "organizer/event_form.html", {"form": form})

#  delete event
#
#(is_admin)
def eventdelete(request, id):
    event = get_object_or_404(Events, id = id)

    if request.method == "POST":
        event.delete()
        return redirect("org-event-list")
    
    return render(request, "organizer/confirm_delete.html", {"obj": event})
def eventdetails(request, id):
    event = get_object_or_404(
        Events.objects.select_related("category").prefetch_related("rsvps"),
        id=id
    )

    try:
        user_rsvp = RSVP.objects.get(user=request.user, event=event)
    except RSVP.DoesNotExist:
        user_rsvp = None

    # RSVP participant list (with status)
    rsvp_participants = RSVP.objects.filter(event=event).select_related('user')

    context = {
        "event": event,
        "user_rsvp": user_rsvp,
        "rsvp_participants": rsvp_participants
    }

    return render(request, "organizer/event_detail.html", context)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'organizer/category_list.html', {'categories': categories})

# Create category
#
#(is_admin)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm()
    return render(request, 'organizer/category_form.html', {'form': form, 'title': 'Create Category'})

# Edit category
#
#(is_admin)
def category_edit(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'organizer/category_form.html', {'form': form, 'title': 'Edit Category'})

# Delete category
#
#(is_admin)
def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('category-list')
    return render(request, 'organizer/confirm_delete.html', {'obj': category})
