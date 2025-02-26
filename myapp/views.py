from django.shortcuts import render

def custompage(request,exception):
      return render(request, '404.html')
    
