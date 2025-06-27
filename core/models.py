from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.company}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class StoreHours(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    day = models.CharField(max_length=10, choices=DAY_CHOICES, blank=True, help_text="Day of the week (leave blank for special/holiday hours)")
    date = models.DateField(blank=True, null=True, help_text="Specific date for special/holiday hours (optional)")
    opening_time = models.TimeField(help_text="Opening time (e.g. 07:00 AM)")
    closing_time = models.TimeField(help_text="Closing time (e.g. 09:30 PM)")
    is_special_day = models.BooleanField(default=False, help_text="Check if this is a special day (e.g. holiday)")
    special_note = models.CharField(max_length=100, blank=True, help_text="Special note for this day (e.g. 'Hours might differ')")
    
    class Meta:
        ordering = ['date', 'day']
    
    def __str__(self):
        if self.date:
            return f"{self.date.strftime('%A, %b %d')} - {self.special_note or 'Special Hours'}"
        if self.is_special_day:
            return f"{self.get_day_display()} - {self.special_note}"
        return f"{self.get_day_display()} {self.opening_time.strftime('%I:%M %p')}–{self.closing_time.strftime('%I:%M %p')}"

class SaleItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='sales/', blank=True, null=True, help_text="Upload a photo of the sale item.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class AboutContent(models.Model):
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"About Us - Updated {self.updated_at.strftime('%B %d, %Y')}"

class Suggestion(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    suggestion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Suggestion from {self.name or 'Anonymous'} - {self.created_at.strftime('%B %d, %Y')}"

class StoreInfo(models.Model):
    name = models.CharField(max_length=200, default="Lucky Twyn Rivers Variety")
    address = models.TextField(default="159 Twyn Rivers Dr, Pickering, ON L1V 1E4")
    phone = models.CharField(max_length=20, default="(905) 509-3328")
    email = models.EmailField(blank=True)
    
    def __str__(self):
        return self.name
