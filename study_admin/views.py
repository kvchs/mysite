from django.shortcuts import render, redirect
from study_admin import models

# Create your views here.


def login(request):
    # models.Administrator.objects.create(
    #     username='admin',
    #     password='adminadmin'
    # )
    message = ''
    if request.method == "POST":
        username = request.POST.get('user')
        password = request.POST.get('pwd')
        c = models.Administrator.objects.filter(username=username, password=password).count()
        if c:
            req = redirect('/study_admin/study-index.html/')
            req.set_cookie('username', username)
            return req
        else:
            message = 'username or password error'
    return render(request, 'study-login.html', {'msg': message})

def study_index(request):
    username = request.COOKIES.get('username')
    if username:
        print(request.COOKIES.get('csrftoken'))
        return render(request, 'study-index.html', {'username': username})
    else:
        return redirect('/study_admin/study-login.html')
    # return render(request, 'study-index.html')