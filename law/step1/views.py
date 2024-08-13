from django.shortcuts import render, redirect # type: ignore
import calendar
from datetime import datetime
from django.http import HttpResponseRedirect # type: ignore
from calendar import HTMLCalendar
from .models import Event, Venue
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponse # type: ignore
import csv
from django.http import FileResponse # type: ignore
import io
from reportlab.pdfgen import canvas # type: ignore
from reportlab.lib.units import inch # type: ignore
from reportlab.lib.pagesizes import letter # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth.models import User # type: ignore


# Create your views here.


from django.core.paginator import Paginator # type: ignore



def admin_approvel(request):
    event_list = Event.objects.all().order_by("-event_date")
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()
    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist('boxes')
            event_list.update(approved=False)
            for x in id_list:
                Event.objects.filter(pk=int(x)).update(approved=True)
                
            messages.success(request, "Event list Approvel")
            return redirect('step1:event_list')
        else:
            return render(request, "step1/admin_approval.html",{
                "event_list" : event_list,
                "event_count": event_count,
                "venue_count": venue_count,
                "user_count" : user_count
            })
    else:
        messages.success(request, "You are not authorized to use this page.")
        return redirect('step1:index') 
    
  
    





def my_events(request):
    
    
    
    if request.user.is_authenticated:
       
        me = request.user.id
        events = Event.objects.filter( attendees=me)
        return render(request, "step1/my_events.html",{
            "events": events,
            
        })
        
    else:
        messages.success(request, ("You Aren't authorized to view this page"))
        return redirect('step1:event_list')




def venue_pdf(request):
    
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    
    venues = Venue.objects.all()
    lines = []
    
    
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append("  ")
       

    for line in lines:
        textob.textLine(line)
        

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    
    return FileResponse(buf, as_attachment=True, filename='venue.pdf')





def venue_csv(request):
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    
    writer = csv.writer(response)
    
    
    venues = Venue.objects.all()
    

    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web Address', 'Email'])


    
    for venue in venues:
        writer.writerow([venue.name, venue.address, venue.phone, venue.web, venue.email_address])
        

  
    return response






def venue_text(request):
    
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    
    venues = Venue.objects.all()
    
    lines = []
    
    for venue in venues:
        lines.append(f'{venue.name}\n{venue.address}\n{venue.phone}\n\n\n')
        

    response.writelines(lines)
    return response



def delete_venue(request, venue_id):
    
       
        venue = Venue.objects.get(pk=venue_id)
        venue.delete()
        return redirect('step1:list_venue')





def delete_event(request, event_id):
    
       event = Event.objects.get(pk=event_id)
       if request.user == event.manager:
            event.delete()
            messages.success(request, ("Event Deleted!"))
            return redirect('step1:event_list')
       else:
           messages.success(request, ("You are not Authorized to delete this event"))
           return redirect('step1:event_list')

    


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('add_event?submitted=True')
        
            
            
        else: 
            form = EventForm(request.POST)
            event = form.save(commit=False)
            event.manager = request.user
            event.save
           
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('add_event?submitted=True')
    else:
        
        if request.user.is_superuser:
                form = EventFormAdmin
        else:
             form = EventForm
        if "submitted" in request.GET:
            submitted = True
   
    return render(request, "step1/add_event.html",{
        "form": form,
        "submitted": submitted
    })



def update_event(request, venue_id):
    
        event = Event.objects.get(pk=venue_id)
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST or None, instance=event)
          
        else:    
            form = EventForm(request.POST or None, instance=event)
        if form.is_valid():
            form.save()
            return redirect('step1:event_list')
        return render(request, "step1/update_event.html",{
            "venue": event,
            "form": form
        })
    



def update_venue(request, venue_id):
    
        venue = Venue.objects.get(pk=venue_id)
        form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
        if form.is_valid():
            form.save()
            return redirect('step1:list_venue')
        return render(request, "step1/update_venue.html",{
            "venue": venue,
            "form": form
        })
    


def search_venues(request):


    
    if request.method == "POST":
        searched = request.POST["searched"]
        Venues = Venue.objects.filter(name__contains=searched)
    
        return render(request, "step1/search_venues.html",{
           "searched": searched,
           "Venues": Venues
        })
        
    else:
        
        
        return render(request, "step1/search_venues.html",{
            
        
            })


def search_events(request):
    
    if request.method == "POST":
        searched = request.POST["searched"]
        events = Event.objects.filter(name__contains=searched)
    
        return render(request, "step1/search_events.html",{
           "searched": searched,
           "events": events
        })
        
    else:
        
        
        return render(request, "step1/search_events.html",{
            
        
            })



def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, "step1/show_venue.html",{
            "venue": venue,
            "venue_owner": venue_owner
        })



def list_venue(request):
      venue_list = Venue.objects.all()
      p = Paginator(Venue.objects.all(), 9)
      page = request.GET.get('page')
      venues = p.get_page(page)
      nums = "a" * venues.paginator.num_pages
      return render(request, "step1/venues.html",{
            "venue_list": venue_list,
            "venues" : venues,
            "nums": nums
        })
    






def add_venue(request):
    submitted = False
    if request.method == "POST":
       
        form = VenueForm(request.POST, request.FILES)
      
        if form.is_valid():
                venue = form.save(commit=False)
                venue.owner = request.user.id
                venue.save()
                return HttpResponseRedirect('add_venue?submitted=True')
    else:
        form = VenueForm       
            
        if "submitted" in request.GET:
            submitted = True
   
    return render(request, "step1/add_venue.html",{
        "form": form,
        "submitted": submitted
    })



def all_events(request):
    event_list = Event.objects.all().order_by('-event_date')
    return render(request, "step1/event_list.html",{
        "event_list":event_list
    })






def index(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    
    cal = HTMLCalendar().formatmonth(year,month_number)
   
    
    event_list = Event.objects.filter(
        event_date__year = year,
        event_date__month= month_number,
    ) 
    
    
    
    return render(request, "step1/index.html",{
        "year":year,
        "month":month,
        "month_number":month_number,
        "cal":cal,
        "event_list": event_list,
    })
