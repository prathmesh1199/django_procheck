from django.db import models
from django.utils import timezone

# Create your models here.
class Group(models.Model) :
    group_id = models.CharField(max_length=10,primary_key=True)
    leader_no = models.CharField(max_length=10)
    division = models.CharField(max_length=1)
    email = models.EmailField()
    password = models.CharField(max_length=50)
      

class Student(models.Model) :
    rollno = models.CharField(max_length=10,primary_key=True)
    grp = models.ForeignKey('Group', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

class Teacher(models.Model) :
    T_id = models.CharField(max_length=10,primary_key=True)
    T_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)    
    
class Project(models.Model) :

    proj_id = models.CharField(max_length=10,primary_key=True)
    grp = models.CharField(max_length = 10)
    title = models.CharField(max_length=50)
    description = models.TextField()
    domain = models.CharField(max_length=50)
    thrust_area = models.CharField(max_length=50)
    status = models.IntegerField(default=0)    