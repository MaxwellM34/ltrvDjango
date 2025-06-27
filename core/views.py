from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Service, BlogPost, Testimonial, Contact, StoreHours, SaleItem, AboutContent, Suggestion, StoreInfo
from .forms import ContactForm, SuggestionForm
from datetime import time

def home(request):
    store_info = StoreInfo.objects.first()
    if not store_info:
        store_info = StoreInfo.objects.create()
    
    # Always use the single AboutContent instance
    about_content, _ = AboutContent.objects.get_or_create(id=1, defaults={
        'content': "Your friendly neighborhood convenience store, serving Pickering for all your daily needs."
    })
    
    # Auto-create default weekly store hours if none exist
    if not StoreHours.objects.filter(date__isnull=True).exists():
        default_hours = [
            ("monday", time(7, 0), time(21, 30)),
            ("tuesday", time(7, 0), time(21, 30)),
            ("wednesday", time(7, 0), time(21, 30)),
            ("thursday", time(7, 0), time(21, 30)),
            ("friday", time(7, 0), time(22, 0)),
            ("saturday", time(7, 0), time(22, 0)),
            ("sunday", time(7, 30), time(21, 30)),
        ]
        for day, open_t, close_t in default_hours:
            StoreHours.objects.create(day=day, opening_time=open_t, closing_time=close_t)
    
    sale_items = SaleItem.objects.filter(is_active=True).order_by('-created_at')
    # Order weekly hours from Monday to Sunday
    day_order = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    weekly_hours = [
        StoreHours.objects.filter(day=day, date__isnull=True).first()
        for day in day_order
    ]
    weekly_hours = [h for h in weekly_hours if h]
    # Get special/holiday hours (with a date)
    special_hours = StoreHours.objects.filter(date__isnull=False).order_by('date')
    
    context = {
        'store_info': store_info,
        'about_content': about_content,
        'sale_items': sale_items,
        'weekly_hours': weekly_hours,
        'special_hours': special_hours,
    }
    return render(request, 'core/home.html', context)

def about(request):
    testimonials = Testimonial.objects.all()
    context = {
        'testimonials': testimonials,
    }
    return render(request, 'core/about.html', context)

def services(request):
    services = Service.objects.all()
    context = {
        'services': services,
    }
    return render(request, 'core/services.html', context)

def blog(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'core/blog.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    context = {
        'post': post,
    }
    return render(request, 'core/blog_detail.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'core/contact.html', context)

def suggestion(request):
    if request.method == 'POST':
        form = SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your suggestion!')
            return redirect('suggestion')
    else:
        form = SuggestionForm()
    
    context = {
        'form': form,
    }
    return render(request, 'core/suggestion.html', context)

@login_required
def admin_panel(request):
    store_info = StoreInfo.objects.first()
    if not store_info:
        store_info = StoreInfo.objects.create()
    
    # Always use the single AboutContent instance
    about_content, _ = AboutContent.objects.get_or_create(id=1)
    
    # Auto-create default weekly store hours if none exist
    if not StoreHours.objects.filter(date__isnull=True).exists():
        default_hours = [
            ("monday", time(7, 0), time(21, 30)),
            ("tuesday", time(7, 0), time(21, 30)),
            ("wednesday", time(7, 0), time(21, 30)),
            ("thursday", time(7, 0), time(21, 30)),
            ("friday", time(7, 0), time(22, 0)),
            ("saturday", time(7, 0), time(22, 0)),
            ("sunday", time(7, 30), time(21, 30)),
        ]
        for day, open_t, close_t in default_hours:
            StoreHours.objects.create(day=day, opening_time=open_t, closing_time=close_t)
    
    store_hours = StoreHours.objects.all()
    sale_items = SaleItem.objects.all()
    suggestions = Suggestion.objects.all().order_by('-created_at')
    
    context = {
        'store_info': store_info,
        'about_content': about_content,
        'store_hours': store_hours,
        'sale_items': sale_items,
        'suggestions': suggestions,
    }
    return render(request, 'core/admin.html', context)
