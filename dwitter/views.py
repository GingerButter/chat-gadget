from django.shortcuts import render, redirect
from django.http import JsonResponse, StreamingHttpResponse
from django.core import serializers
from django.views.decorators import gzip
import cv2
import time

from .forms import DweetForm
from .models import Dweet, Profile


def dashboard(request):
    form = DweetForm(request.POST or None)
    followed_dweets = Dweet.objects.all().order_by("-created_at")
    return render(
        request,
        "dwitter/dashboard1.html",
        {"form": form, "dweets": followed_dweets},
    )

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def dashboardPost(request):
    if is_ajax(request) and request.method == "POST":
        form = DweetForm(request.POST or None)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            # return redirect("dwitter:dashboard")
            ser_instance = serializers.serialize('json', [ dweet, ])
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})


def profile(request, pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "dwitter/profile.html", {"profile": profile})

def postAjax(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = DweetForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400)

class Stream:
    def genPath(self,i):
        return "/home/andyj/Desktop/SLED/chat/dwitter/flower"+str(i)+".png"


    def toBinary(self,path):
        img = cv2.imread(path)
        _, jpeg = cv2.imencode('.png', img)
        return jpeg.tobytes()

def gen(stream):
    for i in range(1,4):
        time.sleep(1)
        path = stream.genPath(i)
        binary = stream.toBinary(path)
        yield (b'--binary\r\n'
               b'Content-Type: image/png\r\n\r\n' + binary + b'\r\n\r\n')

@gzip.gzip_page
def streaming(request):
    try:
        stream = Stream()
        return StreamingHttpResponse(gen(stream), content_type="img/png-replace")
    except:
        pass
    return render(request, "streaming.html")