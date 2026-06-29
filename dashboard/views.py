#imports
from django.shortcuts import render,redirect
import requests
from django.http import JsonResponse
from .services.github_services import checking
from .services.pipeline import startup_doctor

# Special imports
import base64
from groq import Groq
import time
import json

#Global variables
report = None
analysis_complete = False
github_url = None



#Return Landing Page
def index(request):
    return render(request, 'index.html')



def analyzing(request):
    if request.method != "POST": return redirect("index")
    github_url = request.POST.get("github_url")

    if not checking(github_url):
        return render(request, "error.html")

    request.session["github_url"] = github_url
    return render(request, "analyzing.html")

def run_analysis(request):
    global analysis_complete
    global report

    analysis_complete = False
    github_url = request.session.get("github_url")
    report = startup_doctor(github_url)
    analysis_complete = True

    return JsonResponse({'success': True})

def analysis_status(request):
    global analysis_complete

    return JsonResponse({'complete': analysis_complete})

def dashboard(request):
    global report
    print (report)

    return render(request, 'dashboard.html', { 'result' : report })