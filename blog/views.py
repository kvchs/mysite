from django.shortcuts import render, HttpResponse, render_to_response, redirect
from blog import models
import json

from django.template import RequestContext, Template
# Create your views here.
import datetime
# user_list = []


def cur_time(request):
    # return HttpResponse("<h1>ok</h1>")
    time = datetime.datetime.now()
    # print(request.method)
    # return render(request, "cur_time.html",{'abc':time})
    data = "%s" % time
    return HttpResponse(data)


def userInfo(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        sex = request.POST.get("sex", None)
        email = request.POST.get("email", None)

        models.UserInfo.objects.create(
            username=username,
            sex=sex,
            email=email,
        )

        print(username)
        print(sex)
        print(email)
        # user = {'username':username, 'sex':sex, 'email':email}
        # user_list.append(user)
        # return render(request, "index.html", {"user_list": user_list})
        user_list = models.UserInfo.objects.all()
        print(user_list)
    user_list = models.UserInfo.objects.all()
    return render(request, "index.html", {"user_list": user_list})


def special_case_2003(request):
    return HttpResponse('2003')


# year 参数为必填想，不然报错 year_archive() got an unexpected keyword argument 'year'
def year_archive(request, year, month):         # year 参数为必填
    return HttpResponse(str(year) + "|" + str(month))


def article_detail(request, year, month, slug):
    return HttpResponse(str(year) + "|" + str(month) + "|" + slug)


def index(request, name):
    return redirect("http://www.baidu.com")


def index_rename(request):
    print(request.GET)
    print(request.path)       # /blog/index_rename/
    print(request.get_full_path())
    print(request.method)
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username == 'admin' and password == "admin":
            return HttpResponse("successful")

    # return render(request, "login.html")
    name = "charley"
    name2 = "ll1"
    # return render_to_response("login.html", {"name": name,"name2": name2}) # 建议用render，此处有坑
    return render_to_response("login.html", locals())   # 本地变量，可以直接在HTML使用变量,有点影响效率


# def login(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         if username == 'admin' and password == "admin":
#             return redirect("http://www.baidu.com")
#         return redirect("blog/login")
#     return render(request, "login.html")


def login(request):

    if request.method == "POST":
        if True:
            # 用redirect 可以多走一部分逻辑代码
            # return redirect("/blog/homepage")
            return render(request, 'homepage.html', {"name": "charley_chen"})
            # return HttpResponse("{%csrf_token%}：csrf_token标签")
            # return render_to_response('homepage.html', content_type=RequestContext(request))
    return render(request, "login.html")


def homepage(request):
    name = "charley"
    return render(request, 'homepage.html', {'name': name})


def index_template(request):
    class Person(object):
        def __init__(self, name, age):
            self.name = name
            self.age = age
    person = Person('chao', 18)
    s = "hello"
    s_list = [1, 22, 333]
    s_dict = {"username": 'admin','password': '123'}
    s_data = datetime.datetime.now()
    s_url = "<a href='#'>http://www.google.com</a>"
    return render(request, 'index.html', {'list': s_list, 'dict': s_dict, 'date': s_data, 'person': person, 's': s, "url": s_url})


def ordered(request):
    return render(request, 'ordered.html')


def shoppingcart(request):
    return render(request, 'shoppingcart.html')


def data_operation(request):
    # models.BookToAuthor.objects.create(
    #     book_id=2,
    #     author_id=3
    #
    # )
    # test_log = models.Book.objects.filter(id=1)
    # if test_log:
    #     print("ddddddddddddddd")
    # models.Book.objects.filter(id=1).update(title="aaa")
    # if test_log:
    #     print("ddddddddddddddd")
    # test_log = test_log[0]
    return HttpResponse("OK")


def ajax_test(request):

    return render(request, 'ajax-test.html')


def ajax_receive(request):
    if request.method == "POST":
        print(request.POST)
    return HttpResponse("hello ajax")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        print(username)
        if username == "john":
            return HttpResponse("true")

        return HttpResponse("false")
    return render(request, 'register.html')


def jquery_test(request):
    print(request.POST)
    dic = {'name': 'dic_var'}
    HttpResponse.status_code = "400"
    return HttpResponse(json.dumps(dic))


def jquery_html(request):
    return render(request, 'ajax_jquery.html')