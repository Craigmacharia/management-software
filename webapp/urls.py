
from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

from .views import create_assignment, assignments_list


urlpatterns = [

path('',views.home, name=""),

path('register', views.register, name="register"),

path('my-login', views.my_login, name="my-login"),

path('user-logout', views.user_logout, name="user-logout"),

path('contact', views.contact, name="contact"),

path('orientation', views.orientation, name="orientation"),

path('assignments/', views.assignments_list, name='assignments'),


#crud

path('dashboard', views.dashboard, name="dashboard"),

path('create-record', views.create_record, name="create-record"),

    
path('update-record/<int:pk>', views.update_record, name='update-record'),

path('record/<int:pk>', views.singular_record, name="record"),

path('delete-record/<int:pk>', views.delete_record, name="delete-record"),


path('admin-login/', views.admin_login, name='admin-login'),
    
path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),

path('create-assignment/', views.create_assignment, name='create-assignment'),

path('assignments/', views.assignments_list, name='assignments'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.shortcuts import render
from .models import Assignment

def assignments_list(request):
    query = request.GET.get('q')  # Get search query from URL
    if query:
        assignments = Assignment.objects.filter(
            title__icontains=query  # Search by title (case-insensitive)
        ) | Assignment.objects.filter(
            description__icontains=query  # Search by description
        ) | Assignment.objects.filter(
            due_date__icontains=query  # Search by due date (optional)
        )
    else:
        assignments = Assignment.objects.all()  # Show all assignments if no search

    return render(request, 'assignments_list.html', {'assignments': assignments})




