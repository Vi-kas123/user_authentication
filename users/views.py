from django.shortcuts import render, redirect,HttpResponse
from django.contrib import messages,auth
from .models import Patient, Doctor
from django.contrib.auth.decorators import login_required


def register(request):
    return render(request,'register.html')

def signup(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        profile_picture = request.FILES.get('profile_picture')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        address_line1 = request.POST.get('address_line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        if password1 != password2:
            messages.error(request, 'Passwords does not match.')
            return redirect('register')

        if Patient.objects.filter(email=email).exists() or Doctor.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return redirect('register')

        if Patient.objects.filter(username=username).exists() or  Doctor.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('register')

       
        if user_type == 'patient':
            patient = Patient(username=username, email=email, password=password1, first_name=first_name, last_name=last_name, profile_picture=profile_picture, address_line1=address_line1, city=city, state=state, pincode=pincode)
            patient.save()
            messages.success(request, 'Patient User Created Successfully')
            return redirect('login')

        elif user_type == 'doctor':
            doctor = Doctor(username=username, email=email, password=password1, first_name=first_name, last_name=last_name,profile_picture=profile_picture, address_line1=address_line1, city=city, state=state, pincode=pincode)
            doctor.save()
            messages.success(request, 'Doctor User Created Successfully') 
            return redirect('login')

    return render(request, 'register.html')
    

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        # Custom authentication logic based on your models and user type
        user = authenticate_patient_or_doctor(email, password, user_type)

        if user is not None:
            if user_type == 'patient':
                messages.success(request, 'Patient Login Successful')
                return render(request,'dashboard.html',{'user':user})
            elif user_type == 'doctor':
                messages.success(request, 'Doctor Login Successful')
                return render(request,'dashboard.html',{'user':user})
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def authenticate_patient_or_doctor(email, password, user_type):
    try:
        if user_type == 'patient':
            user = Patient.objects.get(email=email)
        elif user_type == 'doctor':
            user = Doctor.objects.get(email=email)
        else:
            return None

        # Verify the password (plaintext check - NOT RECOMMENDED)
        if user.password == password:
            return user
    except (Patient.DoesNotExist, Doctor.DoesNotExist):
        pass

    return None

@login_required(login_url='login')
def logout(request):
      print("lkdsmlknadfnlk")
      auth.logout(request)
      messages.success(request,"You are logged out.")
      print("lkdsmlknadfnlk")
      return redirect('login')