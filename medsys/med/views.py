from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import PIL
import numpy as np

from .Predictions import PneumoniaModel
# Create your views here.
from .form import ImageForm
from .models import *


def About(request):
    return render(request, 'about.html')


def Home(request):
    return render(request, 'home.html')


def Contact(request):
    return render(request, 'contact.html')




def Login(request):
    error = ""
    if request.method == "POST":
        u = request.POST["uname"]
        p = request.POST['pwd']
        user = authenticate(username = u, password = p)
        try:
            if user.is_staff:
                login(request, user)
                error = "No"
            else:
                error = "Yes"
        except:
            error = "Yes"
    d = {'error': error}
    return render(request, 'login.html', d)

def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('login')

    logout(request)
    return redirect('admin_login')


def Predictions(request):
    if request.method == "POST":
        form = ImageForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            return render(request, "predictions.html", {"obj": obj})
    else:
        form = ImageForm()
        #img = Image.objects.all()
    return render(request, "predictions.html", {"form": form})


def upload(request):
    if request.method == 'POST' and 'image' in request.FILES:
        uploaded_file = request.FILES['image']

        image = PIL.Image.open(uploaded_file)

        image.thumbnail((400, 300), resample = PIL.Image.ANTIALIAS)

        resized_image_file = BytesIO()

        image.save(resized_image_file, 'JPEG', quality=90)

        resized_image = InMemoryUploadedFile(resized_image_file, None, 'image.jpg', 'image/jpeg',
                                             resized_image_file.tell(), None)

        fs = FileSystemStorage()
        filename = fs.save(resized_image.name, resized_image)
        uploaded_file_url = fs.url(filename)

        model = PneumoniaModel()

        percentage = model.predict(image)
        print(percentage)
        calc_result = np.round(percentage)
        return render(request, "predictions.html", {
            'uploaded_file_url': uploaded_file_url,
            'uploaded_file_name': uploaded_file.name,
            'calc_result': calc_result
        })
    return render(request, "predictions.html")


def View_Doctor(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Doctor.objects.all()
    d = {'doc': doc}
    return render(request, 'view_doctor.html', d)


def Delete_Doctor(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')


def Add_Doctor(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        n = request.POST["name"]
        m = request.POST['mobile']
        sp = request.POST['special']

        try:
            Doctor.objects.create(name=n, mobile=m, special=sp)
            error = 'No'
        except:
            error = "Yes"
    d = {'error': error}
    return render(request, 'add_doctor.html', d)

def View_Patient(request):
    if not request.user.is_staff:
        return redirect('login')
    pat = Patient.objects.all()
    d = {'doc': pat}
    return render(request, 'view_patient.html', d)

def Delete_Patient(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')

def Add_Patient(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')

    if request.method == "POST":
        n = request.POST["name"]
        g = request.POST["gender"]
        m = request.POST['mobile']
        a = request.POST['address']

        try:
            Patient.objects.create(name=n, gender=g, mobile=m, address=a)
            error = 'No'
        except:
            error = "Yes"
    d = {'error': error}
    return render(request, 'add_patient.html', d)


def Add_Appointment(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')

    doctor1 = Doctor.objects.all()
    patient1 = Patient.objects.all()

    if request.method == "POST":
        n = request.POST["doctor"]
        p = request.POST["patient"]
        dt = request.POST['date']
        t = request.POST['time']
        doctor = Doctor.objects.filter(name=n).first()
        patient = Patient.objects.filter(name=p).first()

        try:
            print(doctor, patient, dt, t)
            Appointment.objects.create(doctors=doctor, patients=patient, date=dt, time=t)
            error = 'No'
        except:
            error = "Yes"

    d = {'doctor': doctor1, 'patient': patient1, 'error': error}
    return render(request, 'add_appointment.html', d)

def View_Appointment(request):
    if not request.user.is_staff:
        return redirect('login')
    pat = Appointment.objects.all()
    d = {'doc': pat}
    return render(request, 'view_appointment.html', d)

def Delete_Appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = Appointment.objects.get(id=pid)
    patient.delete()
    return redirect('view_appointment')