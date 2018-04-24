from django.db import models

# Create your models here.

# Django练习小项目：学员管理系统设计开发
# 带着项目需求学习是最有趣和效率最高的，今天就来基于下面的需求来继续学习Django
#
# 项目需求：
#
# 1.分讲师\学员\课程顾问角色,
# 2.学员可以属于多个班级,学员成绩按课程分别统计
# 3.每个班级至少包含一个或多个讲师
# 4.一个学员要有状态转化的过程 ,比如未报名前,报名后,毕业老学员
# 5.客户要有咨询纪录, 后续的定期跟踪纪录也要保存
# 6.每个学员的所有上课出勤情况\学习成绩都要保存
# 7.学校可以有分校区,默认每个校区的员工只能查看和管理自己校区的学员
# 8.客户咨询要区分来源

# Create your models here.
from django.core.exceptions import ValidationError

from django.db import models
from django.contrib.auth.models import User

class_type_choices= (('online',u'网络班'),
                     ('offline_weekend',u'面授班(周末)',),
                     ('offline_fulltime',u'面授班(脱产)',),
                     )
#1用户表（讲师，销售，课程顾问，学校工作人员）
class UserProfile(models.Model): #UserProfile是对默认基本表User的继承和扩展
    user = models.OneToOneField(User, on_delete=models.CASCADE) #一对一是外键的特例，下拉框选择一次后，下次就不能再次选择 unique
    name = models.CharField(u"姓名",max_length=32)
    #UserProfile相当于用户详细表，User相当于用户基本表（djangomore默认用户表）  这2个表中name=alex只能是一对一
    #在详细表中，创建一条记录是alex，对应基本表的alex；再次创建jack的时候，对应基本表就不能还是alex，必须是jack
    #所以用到的是一对一
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    class Meta: #表中文名在admin显示
        verbose_name = '校内工作人员表'
        verbose_name_plural = "校内工作人员表"

#2校区表
class School(models.Model):
    name = models.CharField(u"校区名称",max_length=64,unique=True) #名字
    addr = models.CharField(u"地址",max_length=128)  #地址
    staffs = models.ManyToManyField('UserProfile',blank=True) #校区和学校工作人员UserProfile 多对多
    #一个校区多个讲师 一个讲师（校长、领导）属于多个校区
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name
    class Meta: #表中文名在admin显示
        verbose_name = '校区表'
        verbose_name_plural = "校区表"

#3课程表
class Course(models.Model):
    name = models.CharField(u"课程名称",max_length=128,unique=True) #课程名字 python linux
    price = models.IntegerField(u"面授价格")  #面授价格
    online_price = models.IntegerField(u"网络班价格") #网络班价格
    brief = models.TextField("课程简介", editable=False) #参数中的"课程简介"就相当于是字段的中文别名，显示在admin页面
    # brief = models.TextField() #参数中的"课程简介"就相当于是字段的中文别名，显示在admin页面
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name  #在admin中每条记录显示课程的名字
    class Meta: #表中文名在admin显示
        verbose_name = '课程表'
        verbose_name_plural = "课程表"

#4班级表
class ClassList(models.Model):
    course = models.ForeignKey('Course',on_delete=models.CASCADE) #外键，对应另外一张表的一条记录，本表显示course_id
    # 班级和课程是一对多，一个课程包含多个班级（python就包含python11期、python12期）
    # 外键，下拉框单选课程
    course_type = models.CharField(u"课程类型",choices=class_type_choices,max_length=32)#对应26行
    # 非外键，下拉框单选（和外键的区别是，外键是取的另外一张表的数据，而非外键单选是取的26行元组中的数据，页面显示元组靠后的元素）
    semester = models.IntegerField(u"学期")  #11期 12期
    start_date = models.DateField(u"开班日期")  #默认必选
    graduate_date = models.DateField(u"结业日期",blank=True,null=True) #允许为空
    teachers = models.ManyToManyField(UserProfile,verbose_name=u"讲师") #字段显示中文在admin  多对多
    #一个班多个老师，一个老师带多个班
    def __unicode__(self):
       return "%s(%s)" %(self.course.name,self.course_type)
    def __str__(self):
       # return "%s[%s](%s)" %(self.course.name,self.semester,self.course_type) #显示元组靠前的元素（offline_weekend）
       return "%s[%s](%s)" %(self.course.name,self.semester,self.get_course_type_display())
       # 显示元组靠后的元素（面授班周末） 显示汉字 get_course_type_display()  其中course_type是字段名
    # 前端html也可以这么写  get_course_type_display  需要去掉小括号

    class Meta: #表中文名，和字段联合惟一
        verbose_name = u'班级列表'
        verbose_name_plural = u"班级列表"  #表名显示中文在admin
        unique_together = ("course","course_type","semester")
        #课程-python 课程类型：面授班 学期：11期  这个3个字段联合惟一（不会出现2个python面授班11期）

#5客户表（学生）
class Customer(models.Model):
    qq = models.CharField(u"QQ号",max_length=64,unique=True) #qq必须有，且惟一
    name = models.CharField(u"姓名",max_length=32,blank=True,null=True) #姓名可以为空，刚刚咨询的时候，一般不说真实名字
    phone = models.BigIntegerField(u'手机号',blank=True,null=True)
    stu_id = models.CharField(u"学号",blank=True,null=True,max_length=64)
    #id = models.CharField(u"身份证号",blank=True,null=True,max_length=128)
    source_type = (('qq',u"qq群"),  #学员渠道
                   ('referral',u"内部转介绍"),
                   ('51cto',u"51cto"),
                   ('agent',u"招生代理"),
                   ('others',u"其它"),
                   )
    source = models.CharField(u'客户来源',max_length=64, choices=source_type,default='qq')
    referral_from = models.ForeignKey('self',verbose_name=u"转介绍自学员",help_text=u"若此客户是转介绍自内部学员,请在此处选择内部学员姓名",blank=True,null=True,related_name="internal_referral", on_delete=models.CASCADE)
    #由谁转介绍的，介绍人也是客户表中的，自关联外键（1对多，1个介绍人介绍多个学员）
    # related_name="internal_referral"  是固定写法，反查用internal_referral字段
    # 通过zhangxiaoyu.referral_from就可以查看张晓宇是谁推荐的（比如廖家发）
    # 通过介绍人廖家发，查廖家发推荐了谁，用liaojiafa.internal_referral反查到（张晓宇）

    course = models.ForeignKey(Course,verbose_name=u"咨询课程", on_delete=models.CASCADE) #外键一对多
    class_type = models.CharField(u"班级类型",max_length=64,choices=class_type_choices)#26行
    customer_note = models.TextField(u"客户咨询内容详情",help_text=u"客户咨询的大概情况,客户个人信息备注等...")
    status_choices = (('signed',u"已报名"),
                      ('unregistered',u"未报名"),
                      ('graduated',u"已毕业"),
                      )   #学员状态
    status = models.CharField(u"状态",choices=status_choices,max_length=64,default=u"unregistered",help_text=u"选择客户此时的状态")
    consultant = models.ForeignKey(UserProfile,verbose_name=u"课程顾问", on_delete=models.CASCADE)
    date = models.DateField(u"咨询日期",auto_now_add=True) #自动加上时间

    class_list = models.ManyToManyField('ClassList',verbose_name=u"已报班级",blank=True)
    #可以为空，如果已经报名了，就选班级 多对多（一个班级多个学员，一个学员报了多个班--dali，下拉框多选）
    #创建学员的时候，选择班级，但是要查每个班级有多少人，就是个反向关联

    def __unicode__(self):
        return "%s,%s" %(self.qq,self.name )
    def __str__(self):
        return "%s,%s" %(self.qq,self.name )
    class Meta: #表中文名在admin显示
        verbose_name = '学员表'
        verbose_name_plural = "学员表"

#6跟踪记录表
class ConsultRecord(models.Model):
    customer = models.ForeignKey(Customer,verbose_name=u"所咨询客户", on_delete=models.CASCADE)
    #一对多，外键，一个学员可以有多条跟踪记录(每个跟踪记录只属于一个学员)
    note = models.TextField(u"跟进内容...")
    status_choices = ((1,u"近期无报名计划"),
                      (2,u"2个月内报名"),
                      (3,u"1个月内报名"),
                      (4,u"2周内报名"),
                      (5,u"1周内报名"),
                      (6,u"2天内报名"),
                      (7,u"已报名"),
                      ) #近期的报名学习计划
    status = models.IntegerField(u"状态",choices=status_choices,help_text=u"选择客户此时的状态")
    consultant = models.ForeignKey(UserProfile,verbose_name=u"跟踪人", on_delete=models.CASCADE)
     #一对多，外键，一个课程顾问可以有多条跟踪记录(每个跟踪记录只属于一个课程顾问)，下拉框是课程顾问（校内工作人员）的名字
    date = models.DateField(u"跟进日期",auto_now_add=True) #自动添加当条记录的跟踪日期
    # (第一次和课程顾问a聊的，2个月内，不管是和谁签的，都算在a上，但是过了2个月，再和课程顾问b聊的，就算在b上了)

    def __unicode__(self): #py2.7
        return u"%s, %s" %(self.customer,self.status)
    def __str__(self):  #py3.5
        # return u"%s, %s" %(self.customer,self.status)  #显示148元组的前面元素-key
        return u"%s, %s" %(self.customer,self.get_status_display())  #显示148元组的后面元素-value
    class Meta:
        verbose_name = u'客户咨询跟进记录'
        verbose_name_plural = u"客户咨询跟进记录"

#7课程记录表
class CourseRecord(models.Model):
    course = models.ForeignKey(ClassList,verbose_name=u"班级(课程)", on_delete=models.CASCADE) #外键，下拉框单选班级 内容从另外一个表取
    day_num = models.IntegerField(u"节次",help_text=u"此处填写第几节课或第几天课程...,必须为数字") #day19
    date = models.DateField(auto_now_add=True,verbose_name=u"上课日期")
    teacher = models.ForeignKey(UserProfile,verbose_name=u"讲师", on_delete=models.CASCADE)  #外键，下拉框单选老师，内容从校内工作人员表取-用户表
    def __unicode__(self):
        return u"%s 第%s天" %(self.course,self.day_num)
    def __str__(self):
        return u"%s 第%s天" %(self.course,self.day_num)  #control控制台 显示pythons12 day19
    class Meta:
        verbose_name = u'上课纪录'
        verbose_name_plural = u"上课纪录"  #表名中文显示
        unique_together = ('course','day_num') #联合惟一  python面授 s12 day19不能出现2个一样的

#8学习记录表（某学员的学习记录表）
class StudyRecord(models.Model):
    course_record = models.ForeignKey(CourseRecord, verbose_name=u"第几天课程", on_delete=models.CASCADE)
    #外键，下拉框单选上课记录（这里不能是一对一，如果是一对一，就意味中只有1个人能来上课 vip了）
    student = models.ForeignKey(Customer,verbose_name=u"学员", on_delete=models.CASCADE)
    # student = models.OneToOneField(Customer,verbose_name=u"学员")
    #外键，下拉框单选学员的名字  每个学员只能有一个学习记录--联合惟一 226行
    record_choices = (('checked', u"已签到"),
                      ('late',u"迟到"),
                      ('noshow',u"缺勤"),
                      ('leave_early',u"早退"),
                      )   #签到记录（下拉框单选，但是区别于外键-外键是从别的表取数据）
    record = models.CharField(u"上课纪录",choices=record_choices,default="checked",max_length=64)
    score_choices = ((100, 'A+'),
                     (90,'A'),
                     (85,'B+'),
                     (80,'B'),
                     (70,'B-'),
                     (60,'C+'),
                     (50,'C'),
                     (40,'C-'),
                     (0,'D'),
                     (-1,'N/A'),
                     (-100,'COPY'),
                     (-1000,'FAIL'),
                     ) #成绩作业记录（下拉框单选，但是区别于外键-外键是从别的表取数据）
    score = models.IntegerField(u"本节成绩",choices=score_choices,default=-1)
    date = models.DateTimeField(auto_now_add=True)  #自动添加日期时间
    note = models.CharField(u"备注",max_length=255,blank=True,null=True)  #备注可以为空

    def __unicode__(self):
        return u"%s,学员:%s,纪录:%s, 成绩:%s" %(self.course_record,self.student.name,self.record,self.get_score_display())
    #self.get_score_display()是为了显示A B+等value 而不是显示100 90分数
    def __str__(self):
        # return u"%s,学员:%s,纪录:%s, 成绩:%s" %(self.course_record,self.student.name,self.record,self.get_score_display())
        return u"%s,学员:%s,纪录:%s, 成绩:%s" %(self.course_record,self.student.name,self.get_record_display(),self.get_score_display())

    class Meta:
        verbose_name = u'学员学习纪录'
        verbose_name_plural = u"学员学习纪录"  #表的中文别名
        unique_together = ('course_record','student') #联合唯一  例如：小宇18天只能上一次，无法在18天上2次
        #student的标识是qq号码

# 学员管理系统表结构















# class UserInfo(models.Model):
#     username = models.CharField(max_length=64)
#     sex = models.CharField(max_length=64)
#     email = models.CharField(max_length=64)
#
#
# class Book(models.Model):
#     title = models.CharField(max_length=64)
#     price = models.IntegerField()
#     color = models.CharField(max_length=64)
#     page_num = models.IntegerField(null=True)
#     publisher = models.ForeignKey("Publish")  # 一对多的关系
#     # 接受对象
#     author = models.ManyToManyField("Author")
#
#
# class Publish(models.Model):
#     name = models.CharField(max_length=64)
#     city = models.CharField(max_length=63)
#
#     def __str__(self):
#         return self.city


#
# 表(模型)的创建：
# 实例：我们来假定下面这些概念，字段和关系
#
# 作者模型：一个作者有姓名。
#
# 作者详细模型：把作者的详情放到详情表，包含性别，email地址和出生日期，作者详情模型和作者模型之间是一对一的关系（one－to－one）（类似于每个人和他的身份证之间的关系），在大多数情况下我们没有必要将他们拆分成两张表，这里只是引出一对一的概念。
#
# 出版商模型：出版商有名称，地址，所在城市，省，国家和网站。
#
# 书籍模型：书籍有书名和出版日期，一本书可能会有多个作者，一个作者也可以写多本书，所以作者和书籍的关系就是多对多的关联关系（many－to－many），一本书只应该由一个出版商出版，所以出版商和书籍是一对多关联关系（one－to－many），也被称作外键。






# from django.db import models


# class Publisher(models.Model):
#     name = models.CharField(max_length=30, verbose_name="名称")
#     address = models.CharField("地址", max_length=50)
#     city = models.CharField('城市', max_length=60)
#     state_province = models.CharField(max_length=30)
#     country = models.CharField(max_length=50)
#     website = models.URLField()
#
#     class Meta:
#         verbose_name = '出版商'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name
#
#
# class Author(models.Model):
#     name = models.CharField(max_length=30)
#
#     def __str__(self):
#         return self.name
#
#
# class AuthorDetail(models.Model):
#     sex = models.BooleanField(max_length=1, choices=((0, '男'), (1, '女'),))
#     email = models.EmailField()
#     address = models.CharField(max_length=50)
#     birthday = models.DateField()
#     author = models.OneToOneField(Author, "on_delete")
#
#
# class Book(models.Model):
#     title = models.CharField(max_length=100)
#     authors = models.ManyToManyField(Author)   # 另外自定义第三张表
#     publisher = models.ForeignKey(Publisher, "on_delete")
#     publication_date = models.DateField()
#     price = models.DecimalField(max_digits=5, decimal_places=2, default=10)
#
#     def __str__(self):
#         return self.title




















# class BookToAuthor(models.Model):
#     author = models.ForeignKey("Author", on_delete=models.CASCADE)
#     book = models.ForeignKey("Book", on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = ["author", "book"] # 联合唯一