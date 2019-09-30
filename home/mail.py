import smtplib
import hashlib
'''
def sendmailtoadmin(id,username,cakename,weight,address,price):
    s1="python3.smtp@gmail.com"
    p="python@123"
    r="mohanashwin999@gmail.com"
    m=
        Subject: Order of {}

        ID:{}
        Cake Name:{}
        Cake Weight:{} kg
        Delivery Address:{}
        Price:{}
    .format(username,id,cakename,weight,address,price)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(s1,p) 
    s.sendmail(s1,r,m) 
    s.quit()
'''
def sendmailtoreceiver(receiver):
    s1="viratrs123@gmail.com"
    p="Anushka@123"
    r=receiver
    m='''
        Your Project has been Approved

    '''
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(s1,p) 
    s.sendmail(s1,r,m) 
    s.quit()


def hash_password(password): 
    #result = hashlib.sha224(password.encode())
    return password 