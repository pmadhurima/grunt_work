from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from webhome.models import CustomerDetails, Details
# from mongoengine import *


def home(request):
    return render(request, "webhome/home.html", {'message': "Kustommade"})


def advice(request):
    if request.method == 'POST':
        form = CustomerDetails(request.POST, request.FILES)
        if form.is_valid():
            name1 = form.cleaned_data['name']
            email1 = form.cleaned_data['email']
            address1 = form.cleaned_data['address']
            phone1 = form.cleaned_data['phone']
            list1 = request.POST.getlist('require')
            str1 = '<br/>'.join(list1)
            detail = Details(name=name1, mail_id=email1, address=address1, phone=phone1, requirements=str1, floor=request.FILES['floor_plan'])
            detail.save()
            res = "thank you <br> " + detail.name + " with email -- " + detail.mail_id + "__<br/>.." + str1 + "<br/>.."
            return HttpResponse(res + " <br/> <br/> and data saved!!!!!!!")
    else:
        form = CustomerDetails()
    return render(request, "webhome/advice.html", {'form': form})


def contact(request):
    if request.method == 'POST':
        form = CustomerDetails(request.POST)
        if form.is_valid():
            name1 = form.cleaned_data['name']
            email1 = form.cleaned_data['email']
            address1 = form.cleaned_data['address']
            phone1 = form.cleaned_data['phone']
            list1 = request.POST.getlist['cbox']
            detail = Details(name=name1, mail_id=email1, address=address1, phone=phone1,)
            detail.save()
            res = "thank you " + detail.name + " with email -- " + detail.mail_id + "__<br/> " + list1
            return HttpResponse(res + " and data saved!!!!!!!")
    else:
        form = CustomerDetails()

    return render(request, 'webhome/contact.html', {'form': form})


def test(request):
    return render(request, "webhome/index.html")
    return HttpResponse("thank you")


def handle_uploaded_file(f):
    with open('D:\new.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def demo(request):
    # return render(request, 'webhome/newfile.html', {'templates_path': settings.TEMPLATE_DIRS})
    return HttpResponse("thank you")
