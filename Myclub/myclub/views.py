from email import message
from pickle import NONE
from urllib import response
from urllib.robotparser import RequestRate
from django.shortcuts import redirect, render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect, FileResponse
from django.urls import is_valid_path
from django.contrib import messages
# Import User Model From Django
from django.contrib.auth.models import User
from matplotlib import lines
from .models import Event
from .models import Venue
from . forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponse
import csv
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
# import pagination stuff

from django.core.paginator import Paginator

# Create My Events Page.
# Show Event


def show_event(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'events/show_event.html', {'event': event})


def venue_events(request, venue_id):
    # Grab the venue
    venue = Venue.objects.get(id=venue_id)
    # Grab the events from that venue
    events = venue.event_set.all()
    if events:
        return render(request, 'events/venue_events.html', {'events': events})
    else:
        messages.success(request, ("That Venue Has No Events"))
        return redirect('admin_approval')


def admin_approval(request):
    # Get the venues
    venue_list = Venue.objects.all()

    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()

    event_list = Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist('boxes')

            # Uncheck all events
            event_list.update(approved=False)
            # Update the database
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)
            messages.success(request, ("Event List Approval Has Been Updated"))
            return redirect('list-events')
        else:
            return render(request, 'events/admin_approval.html', {'event_list': event_list, 'event_count': event_count, 'venue_count': venue_count, 'user_count': user_count, 'venue_list': venue_list})
    else:
        messages.success(request, ("You aren't authorize to look that page"))
        return redirect('index')
    return render(request, 'events/admin_approval.html', {})


def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)
        return render(request, 'events/my_events.html', {'events': events
                                                         })
    else:
        messages.success(
            request, ("You aren't authorized to view this page!"))
        return redirect('index')
# Generate Pdf File Venue List


def venue_pdf(request):
    # Create Bytestream
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textobject = c.beginText()
    textobject.setTextOrigin(inch, inch)
    textobject.setFont("Helvetica", 14)

    # Designate The Model
    venues = Venue.objects.all()

    # Create blank list
    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")

    # Loop
    for line in lines:
        textobject.textLine(line)

    # Finish Up
    c.drawText(textobject)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return something
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')

# Generate Csv File Venue List


def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # Create a csv writer
    writer = csv.writer(response)
    # Designate The Model
    venues = Venue.objects.all()

    # Add column headings to the csv file
    writer.writerow(
        ['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web address'])

    # Loop Thu and output
    for venue in venues:
        writer.writerow([venue.name, venue.address,
                        venue.zip_code, venue.phone, venue.web])

    return response

# Generate Text File Venue List


def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    # Designate The Model
    venues = Venue.objects.all()
    # Create blank list
    lines = []
    # Loop Thu and output
    for venue in venues:
        lines.append(f'{venue}\n')

    """ lines = ['This is line 1\n',
             'This is line 2\n',
             'This is line 3\n',
             'Patryk is awesome'] """

    # Write to TextFile
    response.writelines(lines)
    return response

# Delete an event


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, ("Event Deleted!"))
        return redirect('list-events')
    else:
        messages.success(
            request, ("You aren't authorized to delete this event!"))
        return redirect('list-events')


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue.delete()
    return redirect('list-venues')


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user  # logged in user
                event.save()
                return HttpResponseRedirect('/add_event?submitted')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
        else:
            form = EventForm(request.POST)
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_event.html',
                  {'form': form, 'submitted': submitted})


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventFormAdmin(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'events/update_event.html',
                  {'event': event, 'form': form})


def update_venues(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None,
                     request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'events/update_venues.html',
                  {'venue': venue, 'form': form})


def search_venues(request):
    if request.method == "POST":
        searched = request.POST['Searched']
        venue = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html', {'searched': searched, 'venues': venue})
    else:
        return render(request, 'events/search_venues.html')


def search_events(request):
    if request.method == "POST":
        searched = request.POST['Searched']
        events = Event.objects.filter(name__contains=searched)
        return render(request, 'events/search_events.html', {'searched': searched, 'events': events})
    else:
        return render(request, 'events/search_events.html')


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)

    events = venue.event_set.all()
    return render(request, 'events/show_venue.html',
                  {'venue': venue, 'venue_owner': venue_owner, 'events': events})


def list_venues(request):
    venue_list = Venue.objects.all()

    # Set up Pagination
    p = Paginator(Venue.objects.all(), 2)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages

    return render(request, 'events/venue.html',
                  {'venue_list': venue_list,
                   'venues': venues,
                   'nums': nums})


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id  # logged in user
            venue.save()
            return HttpResponseRedirect('/add_venue?submitted')
    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'events/add_venue.html',
                  {'form': form, 'submitted': submitted})


def all_events(request):
    event_list = Event.objects.all().order_by('-event_date',)
    return render(request, 'events/events_list.html',
                  {'event_list': event_list})


def index(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = 'John'
    month = month.capitalize()
    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    cal = HTMLCalendar().formatmonth(year, month_number)
    now = datetime.now()
    current_year = now.year
    current_day = now.day
    current_month = now.strftime('%I')

    # Query the Events For Dates
    event_list = Event.objects.filter(
        event_date__year=year,
        event_date__month=month_number
    )

    return render(request, 'events/index.html', {'name': name, 'year': year, 'month': month, "month_number": month_number, "cal": cal, 'current_year': current_year, 'current_day': current_day, 'current_month': current_month, 'event_list': event_list})
