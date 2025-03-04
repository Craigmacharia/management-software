from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Record, Assignment, Question, Answer, Admin
from .forms import (
    CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm,
    AssignmentForm, QuestionForm, AnswerForm, AdminLoginForm
)

# --------------------------------
# User Authentication Views
# --------------------------------

def home(request):
    return render(request, 'webapp/index.html')

def register(request):
    form = CreateUserForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully!")
        return redirect("my-login")
    return render(request, 'webapp/register.html', {'form': form})

def my_login(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            request, 
            username=form.cleaned_data['username'], 
            password=form.cleaned_data['password']
        )
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'dashboard'))
        messages.error(request, "Invalid username or password.")
    return render(request, 'webapp/my-login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect("")

# --------------------------------
# Dashboard & Records Management
# --------------------------------

@login_required(login_url='my-login')
def dashboard(request):
    records = Record.objects.all()
    return render(request, 'webapp/dashboard.html', {'records': records})

@login_required(login_url='my-login')
def create_record(request):
    form = CreateRecordForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Record created successfully!")
        return redirect("dashboard")
    return render(request, 'webapp/create-record.html', {'form': form})

@login_required(login_url='my-login')
def update_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    form = UpdateRecordForm(request.POST or None, instance=record)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Record updated successfully!")
        return redirect("dashboard")
    return render(request, 'webapp/update-record.html', {'form': form, 'record': record})

@login_required(login_url='my-login')
def delete_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    if request.method == "POST":
        record.delete()
        messages.success(request, "Record deleted successfully!")
        return redirect("dashboard")
    return render(request, 'webapp/delete-record.html', {'record': record})

@login_required(login_url='my-login')
def singular_record(request, pk):
    record = get_object_or_404(Record, id=pk)
    return render(request, 'webapp/view-record.html', {'record': record})

# --------------------------------
# Assignments Management
# --------------------------------

@login_required(login_url='my-login')
def assignments_list(request):
    query = request.GET.get('q', '')
    assignments = Assignment.objects.filter(title__icontains=query) if query else Assignment.objects.all()
    return render(request, 'webapp/assignments.html', {'assignments': assignments})

@login_required(login_url='my-login')
@user_passes_test(lambda u: u.is_superuser)  # Only admin can create assignments
def create_assignment(request):
    form = AssignmentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Assignment created successfully!")
        return redirect('admin-dashboard')
    return render(request, 'webapp/create-assignment.html', {'form': form})

# --------------------------------
# Questions & Answers
# --------------------------------

@login_required(login_url='my-login')
def question_list(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'questions/question_list.html', {'questions': questions})




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .forms import AnswerForm

@login_required(login_url='my-login')
def question_detail(request, pk):
    question = get_object_or_404(Question, id=pk)  # ✅ Use pk instead of question_id
    answers = question.answers.all()  # ✅ Fetch related answers

    form = AnswerForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        answer = form.save(commit=False)
        answer.user = request.user
        answer.question = question
        answer.save()
        return redirect('question_detail', pk=question.id)  # ✅ Use pk=question.id

    return render(request, 'questions/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })





@login_required(login_url='my-login')
def ask_question(request):
    form = QuestionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        question = form.save(commit=False)
        question.user = request.user
        question.save()
        return redirect('question_list')
    return render(request, 'questions/ask_question.html', {'form': form})





@login_required
def answer_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    
    if request.method == "POST":
        Answer.objects.create(
            question=question, 
            user=request.user, 
            body=request.POST.get("answer", "")
        )
        return redirect('question_detail', pk=pk)
    
    return render(request, 'questions/answer_question.html', {'question': question})  # ✅ Ensure this path is correct




# --------------------------------
# Admin Views
# --------------------------------



\
def admin_login(request):
    form = AdminLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username, password = form.cleaned_data['username'], form.cleaned_data['password']
        try:
            admin = Admin.objects.get(username=username)
            if admin.password == password:  # ⚠️ Use password hashing in production
                request.session['admin_id'] = admin.id
                return redirect('admin-dashboard')
            messages.error(request, "Invalid password.")
        except Admin.DoesNotExist:
            messages.error(request, "Admin does not exist.")
    return render(request, 'webapp/admin-login.html', {'form': form})

def admin_dashboard(request):
    if 'admin_id' not in request.session:
        return redirect('admin-login')
    records = Record.objects.all()
    return render(request, 'webapp/admin-dashboard.html', {'records': records})

# Special Admin-Only Views

def is_special_admin(user):
    return user.is_authenticated and user.username in ['CraigMacharia', 'craig']

@user_passes_test(is_special_admin)
def create_record_admin(request):
    return create_record(request)

@user_passes_test(is_special_admin)
def update_record_admin(request, pk):
    return update_record(request, pk)

@user_passes_test(is_special_admin)
def delete_record_admin(request, pk):
    return delete_record(request, pk)

# --------------------------------
# Static Pages
# --------------------------------

def contact(request):
    return render(request, 'webapp/contact.html')

def orientation(request):
    return render(request, 'webapp/orientation.html')






from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .mpesa_utils import lipa_na_mpesa

@csrf_exempt
def initiate_payment(request):
    """Handles MPESA STK Push when 'Pay Now' button is clicked"""
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")
        amount = request.POST.get("amount")

        if not phone_number or not amount:
            return JsonResponse({"error": "Phone number and amount are required"}, status=400)

        response = lipa_na_mpesa(phone_number, amount)
        return JsonResponse(response)

    return JsonResponse({"error": "Invalid request method"}, status=405)





from django.shortcuts import render

def home(request):
    return render(request, "webapp/index.html")  # Make sure 'home.html' exists in templates




from django.http import JsonResponse
import json

def mpesa_callback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("MPESA CALLBACK DATA:", data)  # Debugging
            return JsonResponse({"message": "Callback received"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=400)

