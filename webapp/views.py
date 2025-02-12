

from django.shortcuts import render, redirect,get_object_or_404
from django.shortcuts import render, redirect

from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth

from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Record

from django.contrib import messages

from .models import Admin
from .forms import AdminLoginForm

from .models import Admin, Record

from django.shortcuts import redirect

from .models import Record


from django.contrib.auth import authenticate, login
from .forms import LoginForm

from django.contrib.auth.decorators import user_passes_test

from .forms import CreateRecordForm

from .models import Assignment

from .forms import AssignmentForm




def my_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'dashboard')  # Get the 'next' parameter or default to 'dashboard'
                return redirect(next_url)  # Redirect to the 'next' URL
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = LoginForm()

    return render(request, 'webapp/my-login.html', {'form': form})


#homepage

def home(request):

    return render(request, 'webapp/index.html')


#register

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)
        if form.is_valid():

         form.save()

        return redirect('my-login')


    context = {'form':form}

    return render(request, 'webapp/register.html', context=context)

#login

def my_login(request):
   
   form = LoginForm()

   if request.method == "POST":
      
      form = LoginForm(request, data=request.POST)

      if form.is_valid():
         
         username = request.POST.get('username')
         password = request.POST.get('password')

         user = authenticate(request, username=username, password=password)

         if user is not None:
            
            auth.login(request, user)

            return redirect("dashboard")

   context = {'form':form}

   return render(request, 'webapp/my-login.html', context=context)

#logout
def user_logout(request):
   
   auth.logout(request)

   return redirect("")

#dashboard

@login_required(login_url='my-login')

def dashboard(request):
       
       my_records = Record.objects.all()

       context = {'records': my_records}

   
       return render(request, 'webapp/dashboard.html', context=context)

from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Record

from django.contrib import messages




# - Homepage 

def home(request):

    return render(request, 'webapp/index.html')


# - Register a user

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Account created successfully!")

            return redirect("my-login")

    context = {'form':form}

    return render(request, 'webapp/register.html', context=context)


# - Login a user

def my_login(request):

    form = LoginForm()

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")

    context = {'form':form}

    return render(request, 'webapp/my-login.html', context=context)


# - Dashboard

@login_required(login_url='my-login')
def dashboard(request):

    my_records = Record.objects.all()

    context = {'records': my_records}

    return render(request, 'webapp/dashboard.html', context=context)


# - Create a record 

@login_required(login_url='my-login')
def create_record(request):

    form = CreateRecordForm()

    if request.method == "POST":

        form = CreateRecordForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was created!")

            return redirect("dashboard")
        

   # - Update a record 

@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)

    form = UpdateRecordForm(instance=record)

    if request.method == 'POST':

        form = UpdateRecordForm(request.POST, instance=record)

        if form.is_valid():

            form.save()

            messages.success(request, "Your record was updated!")

            return redirect("dashboard")
        
    context = {'form':form}

    return render(request, 'webapp/update-record.html', context=context)

# - Read / View a singular record

@login_required(login_url='my-login')
def singular_record(request, pk):

    all_records = Record.objects.get(id=pk)

    context = {'record':all_records}

    return render(request, 'webapp/view-record.html', context=context)

# - Delete a record

@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)

    record.delete()

    messages.success(request, "Your record was deleted!")

    return redirect("dashboard")


#contact

def contact(request):

    return render(request, 'webapp/contact.html')


#orientation

def orientation(request):

    return render(request, 'webapp/orientation.html')

#admin only

def admin_login(request):
    if request.method == "POST":
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                admin = Admin.objects.get(username=username)
                if admin.password == password:  # Replace with password hashing in production
                    request.session['admin_id'] = admin.id  # Store admin ID in session
                    return redirect('admin-dashboard')
                else:
                    messages.error(request, "Invalid password.")
            except Admin.DoesNotExist:
                messages.error(request, "Admin does not exist.")
        else:
            messages.error(request, "Invalid form data.")
    else:
        form = AdminLoginForm()

    return render(request, 'webapp/admin-login.html', {'form': form})



def admin_dashboard(request):
    if 'admin_id' not in request.session:  # Check if admin is logged in
        return redirect('admin-login')

    records = Record.objects.all()  # Fetch all records
    return render(request, 'webapp/admin-dashboard.html', {'records': records})






# Custom function to check if the user is the special admin

def is_special_admin(user):
    special_admins = ['CraigMacharia', 'craig']
    return user.is_authenticated and user.username in special_admins



# Apply the decorator to your views
@user_passes_test(is_special_admin)
def create_record(request):
    if request.method == "POST":
        form = CreateRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Record created successfully!")
            return redirect('admin-dashboard')
    else:
        form = CreateRecordForm()
    return render(request, 'webapp/create-record.html', {'form': form})

@user_passes_test(is_special_admin)
def update_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    if request.method == "POST":
        form = CreateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully!")
            return redirect('admin-dashboard')
    else:
        form = CreateRecordForm(instance=record)
    return render(request, 'webapp/update-record.html', {'form': form})

@user_passes_test(is_special_admin)
def delete_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    if request.method == "POST":
        record.delete()
        messages.success(request, "Record deleted successfully!")
        return redirect('admin-dashboard')
    return render(request, 'webapp/delete-record.html', {'record': record})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from .models import Assignment
from .forms import AssignmentForm

# Admin Check
def is_special_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required(login_url='my-login')
@user_passes_test(is_special_admin)
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment created successfully!")
            return redirect('admin-dashboard')  # Ensure 'admin-dashboard' is correctly named in urls.py
    else:
        form = AssignmentForm()
    return render(request, 'webapp/create-assignment.html', {'form': form})


# View Assignments (For Students & Admin)
@login_required(login_url='my-login')
def assignments_list(request):
    assignments = Assignment.objects.all().order_by('-created_at')
    return render(request, 'webapp/assignments.html', {'assignments': assignments})

from django.shortcuts import render
from .models import Assignment  # Import the Assignment model

def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'webapp/assignments.html', {'assignments': assignments})



@login_required(login_url='my-login')
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment created successfully!")
            return redirect('admin-dashboard')
    else:
        form = AssignmentForm()
    return render(request, 'webapp/create-assignment.html', {'form': form})



@login_required(login_url='my-login')
def update_record(request, pk):
    record = get_object_or_404(Record, id=pk)  # Ensure record exists
    form = UpdateRecordForm(instance=record)

    if request.method == "POST":
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect("record", pk=record.pk)  # Ensure redirection to singular_record

    context = {'form': form, 'record': record}  # Ensure record is passed
    return render(request, 'webapp/update-record.html', context)




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Assignment

@login_required  # Ensures only logged-in users can access
def assignments_view(request):
    query = request.GET.get('q', '')
    assignments = Assignment.objects.all()

    if query:
        assignments = assignments.filter(title__icontains=query)

    return render(request, 'webapp/assignments.html', {'assignments': assignments})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Assignment

@login_required
def assignments_view(request):
    query = request.GET.get('q', '')  # Get the search query from URL
    assignments = Assignment.objects.all()

    if query:
        assignments = assignments.filter(title__icontains=query)  # Filter assignments

    return render(request, 'webapp/assignments.html', {'assignments': assignments, 'query': query})






