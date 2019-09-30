from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection
from .models import *
from django.contrib import messages
from matplotlib import pylab
from pylab import *
from django.core.mail import send_mail

#from .mail import *

# Create your views here.
group_login = {'group_id':'','division':'','email':'','loginstatus':False}
admin_login = {'t_id' : '','t_name':'','t_status':False}
stud_list = []
roll_list = []
project_info_id = [] 

def gr_signup(req) :
    if req.method == 'POST' :
        gr = Group()
        st = Student()

        gr.group_id = req.POST.get("group_id")
        gr.leader_no = req.POST.get('leader_rollno')
        gr.division = req.POST.get('div')
        gr.email = req.POST.get('email')
        gr.password = req.POST.get('password')

        group_rows = Group.objects.raw('Select * from home_group')
        for i in group_rows :
            if i.group_id == gr.group_id:
                return render(req,'home/group_signup.html', {'error':'Group Id already in use'})

        gr.save()        
        
        st.rollno = req.POST.get('roll1')
        st.name = req.POST.get('stud1')
        st.grp = gr
        st.save()
        
        st.rollno = req.POST.get('roll2')
        st.name = req.POST.get('stud2')
        st.grp = gr
        st.save()

        st.rollno = req.POST.get('leader_rollno')
        st.name = req.POST.get('group_leader')
        st.grp = gr
        st.save()

        st.rollno = req.POST.get('roll3')
        st.name = req.POST.get('stud3')
        st.grp = gr
        st.save()

        return redirect('home:group_login')
    else:
        return render(req,'home/group_signup.html')

def gr_login(req) :

    
    if req.method == 'POST' :
         
        stud_list.clear()
        roll_list.clear()

        g_id = req.POST.get('group_id'),
        pwd = req.POST.get('group_password'),        
       
        try:
            loginuser = Group.objects.raw('select * from home_group where group_id = %s',[g_id])[0]
        except:
            return render(req,'home/group_login.html',{'error':'NO such group present !'})
        

        if loginuser:
            if pwd[0] == loginuser.password:
                group_login['group_id'] = loginuser.group_id
                group_login['division'] = loginuser.division
                group_login['email'] = loginuser.email
                group_login['loginstatus'] = True
                
                
                query = Student.objects.raw('select * from home_student where grp_id = %s',[group_login['group_id']])
                for i in query:
                    stud_list.append(i.name)
                    roll_list.append(i.rollno)


                return redirect('home:group_info')
            else:
                return render(req,'home/group_login.html',{'error':'Invalid password'})        
        
    else :
        return render(req,'home/group_login.html')


    


def gr_logout(req) :

    if group_login['loginstatus'] == True:
        group_login['group_id'] = ""
        group_login['division'] = ""
        group_login['email'] = ""
        group_login['loginstatus'] = False
        
        stud_list.clear()
        roll_list.clear()

        return redirect('home:group_login')

def teacher_logout(req) :  

    if admin_login['t_status'] == True:
        admin_login['t_id'] = ""
        admin_login['t_name'] = ""
        admin_login['t_status'] = False
        return redirect('home:teacher_login') 


def teacher_login(req) :

    if req.method == 'POST' :
            
        teacher_id = req.POST.get('teacher_id'),
        pwd = req.POST.get('teacher_password'),   

        try:
            loginuser = Teacher.objects.raw('select * from home_teacher where T_id = %s',[teacher_id])[0]
            print(loginuser.T_id)
        except:
            return render(req,'home/teacher_login.html',{'error':'NO such teacher present'})
        

        if loginuser:
            if pwd[0] == loginuser.password:
                admin_login['t_id'] = loginuser.T_id
                admin_login['t_name'] = loginuser.T_name
                admin_login['status'] = True
                return redirect('home:teacher_project_page')
            else:
                return render(req,'home/teacher_login.html',{'error':'Invalid password'})        

    else :
        return render(req,'home/teacher_login.html')
         

def index(req) :
    stud_list.clear()
    roll_list.clear()
    return render(req,'home/index.html') 

def add_projects(req) :

    if req.method == "POST":
        project = Project() 
        count = 0
        it = Project.objects.raw('Select * from home_project')
        
        for i in it:
            count+=1

        id = count + 1000

        
        
        project.proj_id = id
        project.grp = group_login['group_id']
        project.title = req.POST.get('project_title')
        project.domain = req.POST.get('domain')
        project.thrust_area = req.POST.get('area')
        project.description = req.POST.get('description')
        project.status = 1
        
        project_rows = Project.objects.raw('Select * from home_project')
        for i in project_rows :
            if i.grp == project.grp:
                return render(req,'home/add_projects.html', {'error':'YOU CAN ADD ONLY ONE PROJECT'})

        
        project.save()
        return redirect('home:group_info') 
    else:
        return render(req,'home/add_projects.html')    


def group_statistics(req) :
    return render(req,'home/group_statistics.html')

def teacher_statistics(req) :
    return render(req,'home/teacher_statistics.html')

def group_project_page(req) :
    if req.method == 'POST' :
        '''group_id = req.POST['group_id'] 
        print(group_id)
        with connection.cursor() as cursor:
            cursor.execute('update home_project set status = true where grp = %s',[group_id])
        query = Project.objects.raw('select * from home_project where status = 0')        
        query1 = Project.objects.raw('select * from home_project where status = 1')
        return render(req,'home/teacher_project_page.html',{'query':query,'query1':query1})  
        '''
        pass      
    elif req.method == 'GET':
        query = Project.objects.raw('select * from home_project where status = 1')        
        query1 = Project.objects.raw('select * from home_project where status = 2')
        return render(req,'home/group_project_page.html',{'query':query,'query1':query1})    
    
def teacher_project_page(req) :
    
    if req.method == 'POST' :
        if 'group_id' in req.POST:
            #code for approval
            group_id = req.POST['group_id']
            with connection.cursor() as cursor:
                cursor.execute('update home_project set status = 2 where grp = %s',[group_id])
                
                #sendmailtoreceiver('sanketsandream11@gmail.com')
                
                send_mail('HI...!!!',
                'Your Project has been Approved...!!!',
                'viratrs123@gmail.com',
                ['sanketsandream11@gmail.com'],
                fail_silently = False)


                

                print("hello")
        elif 'reject_btn' in  req.POST:
            #code for rejection
            group_id = req.POST['reject_btn']
            with connection.cursor() as cursor:
                cursor.execute('update home_project set status = 3 where grp = %s',[group_id])
        elif 'info_btn' in req.POST:
            group_login['group_id'] = ""
            group_login['division'] = ""
            group_login['email'] = ""
            stud_list.clear()
            roll_list.clear()
            project_info_id.clear()
            project_info_id.append(req.POST['info_btn'])
            #query1 = Project.objects.raw('select * from home_project where grp = %s',[group_id])[0]
            #query2 = Group.objects.raw('select * from home_group where group_id = %s',[group_id])[0]
            #query3 = Group.objects.raw('select * from home_student where grp_id = %s'),[group_id]
            
            print(project_info_id)
            return  redirect('home:project_info')
            #return render(req,'home/teacher_project_page.html',{'description':query1.description})  
        elif 'info_btn1' in req.POST:
            group_login['group_id'] = ""
            group_login['division'] = ""
            group_login['email'] = ""
            stud_list.clear()
            roll_list.clear()
            project_info_id.clear()
            project_info_id.append(req.POST['info_btn1'])
            #query1 = Project.objects.raw('select * from home_project where grp = %s',[group_id])[0]
            #query2 = Group.objects.raw('select * from home_group where group_id = %s',[group_id])[0]
            #query3 = Group.objects.raw('select * from home_student where grp_id = %s'),[group_id]
            
            print(project_info_id)
            return  redirect('home:project_info')
            #return render(req,'home/teacher_project_page.html',{'description':query1.description})  

        query = Project.objects.raw('select * from home_project where status = 1')        
        query1 = Project.objects.raw('select * from home_project where status = 2')
        return render(req,'home/teacher_project_page.html',{'query':query,'query1':query1})        
    elif req.method == 'GET':
        query = Project.objects.raw('select * from home_project where status = 1')        
        query1 = Project.objects.raw('select * from home_project where status = 2')
        return render(req,'home/teacher_project_page.html',{'query':query,'query1':query1})    
     
def project_info(req) :
    print(project_info_id[0])
    group_row = Group.objects.raw('select * from home_group')
    for i in group_row:
        if i.group_id == project_info_id[0]:
            group_login['group_id'] = i.group_id
            group_login['division'] = i.division
            group_login['email'] = i.email
    
    query = Student.objects.raw('select * from home_student where grp_id = %s',[group_login['group_id']])
    for i in query:
        stud_list.append(i.name)
        roll_list.append(i.rollno)
    print(stud_list)
    print(roll_list)
    print(group_login)
    project_rows = Project.objects.raw('Select * from home_project ')
    for i in project_rows :
        if i.grp == group_login['group_id']:
            return render(req,'home/project_info.html',{'group_id': group_login['group_id'],'div': group_login['division'],'n1': stud_list[0],'r1': roll_list[0],'n2': stud_list[1],'r2': roll_list[1],'n3': stud_list[2],'r3': roll_list[2],'n4': stud_list[3],'r4': roll_list[3],'email':group_login['email'],'title':i.title,'id':i.proj_id,'domain':i.domain,'area':i.thrust_area,'description':i.description,'status':i.status})    

    return render(req,'home/project_info.html')

def group_info(req) :
    if group_login['loginstatus'] == True:
        if req.method == 'POST':
            with connection.cursor() as cursor:
               cursor.execute('delete from home_project where grp = %s',[group_login['group_id']])

            return render(req,'home/group_info.html',{'group_id': group_login['group_id'],'div': group_login['division'],'n1': stud_list[0],'r1': roll_list[0],'n2': stud_list[1],'r2': roll_list[1],'n3': stud_list[2],'r3': roll_list[2],'n4': stud_list[3],'r4': roll_list[3],'email':group_login['email'],'title':"You didn't add any Project..."})    

        else :
             
            project_rows = Project.objects.raw('Select * from home_project ')
            for i in project_rows :
                #flag = False
                if i.grp == group_login['group_id']:
                    #flag = True
                    return render(req,'home/group_info.html',{'group_id': group_login['group_id'],'div': group_login['division'],'n1': stud_list[0],'r1': roll_list[0],'n2': stud_list[1],'r2': roll_list[1],'n3': stud_list[2],'r3': roll_list[2],'n4': stud_list[3],'r4': roll_list[3],'email':group_login['email'],'title':i.title,'id':i.proj_id,'domain':i.domain,'area':i.thrust_area,'description':i.description,'status':i.status})    
                    #{'title':i.title,'id':i.proj_id,'domain':i.domain,'area':i.thrust_area,'description':i.description}
                    
            #if flag == False:
                #{'title':"You didn't add any Project..."}

            return render(req,'home/group_info.html',{'group_id': group_login['group_id'],'div': group_login['division'],'n1': stud_list[0],'r1': roll_list[0],'n2': stud_list[1],'r2': roll_list[1],'n3': stud_list[2],'r3': roll_list[2],'n4': stud_list[3],'r4': roll_list[3],'email':group_login['email'],'title':"You didn't add any Project..."})    

    else :
        return render(req,'home/group_info.html')


def domain_statistics(req) :
    
        rows = Project.objects.raw('Select * from home_project where status = 2')

        domains = ['BlockChain','Data Analysis','Web Development','Computer Networks','Machine Learning','Cyber Security','Other']
        
        x=[0,0,0,0,0,0,0]   #initial count of every domain is set to zero

        # to count number of projects in that domain.    
        for i in rows:
            if i.domain == "BlockChain":
                x[0]+=1
            if i.domain == "Data Analysis":
                x[1]+=1
            if i.domain == "Web Development":
                x[2]+=1
            if i.domain == "Computer Networks":
                x[3]+=1
            if i.domain == "Machine Learning":
                x[4]+=1
            if i.domain == "Cyber Security":
                x[5]+=1
            if i.domain == "Other":
                x[6]+=1                        

       

        index = np.arange(len(domains))
        plt.bar(index, x)
        plt.xlabel('Domains', fontsize=5)
        plt.ylabel('Number of groups', fontsize=5)
        plt.xticks(index, domains, fontsize=10)
        plt.title('Domain Wise')
        plt.show()
        
        if group_login['loginstatus'] == True :
            return render(req,'home/group_statistics.html')
        else:
            return render(req,'home/teacher_statistics.html')



def thrust_statistics(req) :
    
        rows = Project.objects.raw('Select * from home_project where status = 2 ')

        areas = ['Industry','Quality Education','Agriculture','Transportation','Sanitation','Other']
        
        x=[0,0,0,0,0,0]   #initial count of every Thrust area is set to zero

        # to count number of projects in that Thrust area.    
        for i in rows:
            if i.thrust_area == "Industry":
                x[0]+=1
            if i.thrust_area == "Quality Education":
                x[1]+=1
            if i.thrust_area == "Agriculture":
                x[2]+=1
            if i.thrust_area == "Transportation":
                x[3]+=1
            if i.thrust_area == "Sanitation":
                x[4]+=1
            if i.thrust_area == "Other":
                x[5]+=1
                                       

        index = np.arange(len(areas))
        plt.bar(index, x)
        plt.xlabel('Thrust Area', fontsize=5)
        plt.ylabel('Number of groups', fontsize=5)
        plt.xticks(index, areas, fontsize=10)
        plt.title('Thrust Wise')
        plt.show()
        if group_login['loginstatus'] == True :
            return render(req,'home/group_statistics.html')
        else:
            return render(req,'home/teacher_statistics.html')

def division_statistics(req):
    rows = Group.objects.raw('select * from home_group,home_project where home_group.group_id = home_project.grp' )
    div = ['A','B','C']

    x=[0,0,0]

    for i in rows:
        if i.division == 'A':
            x[0]+=1
        if i.division == 'B':
            x[1]+=1
        if i.division == 'C':
            x[2]+=1        

    index = np.arange(len(div))
    plt.bar(index, x)
    plt.xlabel('Division', fontsize=5)
    plt.ylabel('Number of groups', fontsize=5)
    plt.xticks(index, div, fontsize=10)
    plt.title('Division Wise')
    plt.show()
    if group_login['loginstatus'] == True :
        return render(req,'home/group_statistics.html')
    else:
        return render(req,'home/teacher_statistics.html')


