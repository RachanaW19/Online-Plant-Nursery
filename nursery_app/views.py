from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Plant,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail


# Create your views here.

def home(request):
    # userid=request.user.id
    # print(userid)
    # print("Result is:",request.user.is_authenticated)
    context={}
    p=Plant.objects.filter(is_active=True)
    # print(p)
    context['plants']=p
    return render(request,'index.html',context)

def plant_details(request,pid):
    p=Plant.objects.filter(id=pid)
    # print(p)
    context={}
    context['plants']=p
    return render(request,'plant_details.html',context)

def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=='' or upass=='' or ucpass=='':
            context['errmsg']="Fields cannot be empty"
        elif upass != ucpass:
            context['errmsg']="Password & confirm didn't match"
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)
                u.save()
                context['success']="User created successfully, Please login"
            except Exception:
                context['errmsg']="User with same username already exists!!"
        # return HttpResponse("User created succefully!!")
        return render(request,'register.html',context)
    else:
        return render(request,'register.html')
    
def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        # print(uname,'-',upass)
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Fields cannot be Empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)
                return redirect('/')  
            else:
                context['errmsg']="Invalid username and password"  
                return render(request,'login.html',context)   
    else:
        return render(request,'login.html')
    
def user_logout(request):
    logout(request)
    return redirect('/')

def catfilter(request,cv):
    q1=Q(cat=cv)
    q2=Q(is_active=True)
    p=Plant.objects.filter(q1&q2)
    print(p)
    context={}
    context['plants']=p
    return render(request,'index.html',context)

def sort(request,sv):
    if sv=='0':
        #ascending
        col='price'
    else:
        #descending
        col='-price'
    p=Plant.objects.order_by(col)
    context={}
    context['plants']=p
    return render(request,'index.html',context)

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    # print(min)
    # print(max)
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=Plant.objects.filter(q1&q2&q3)
    context={}
    context['plants']=p
    return render(request,'index.html',context)

def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        # print(pid)
        # print(userid)
        u=User.objects.filter(id=userid)
        print(u)
        p=Plant.objects.filter(id=pid)
        #check plant exist or not
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        print(c)  #queryset[<object 3>]
        n=len(c)
        context={}
        if n == 1:
            context['msg']="Product already exist in the cart!!"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()           
            context['success']="Plant Added successfully to Cart!!"
        context['plants']=p
        return render(request,'plant_details.html',context)
        # return HttpResponse("Plant added to cart")
    else:
        return redirect('/login')
    

def viewcart(request):
    c=Cart.objects.filter(uid=request.user.id)
    # print(c)
    np=len(c)
    s=0
    for x in c:
        s = s + x.pid.price * x.qty
    print(s)  
    context={}
    context['data']=c
    context['total']=s
    context['n']=np
    return render(request,'cart.html',context)

def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')

def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    print(c)
    print(c[0])
    print(c[0].qty)
    if qv == '1':
        t=c[0].qty + 1
        c.update(qty=t)        
    else:
        if c[0].qty > 1:
            t=c[0].qty - 1
            c.update(qty=t)
    return redirect('/viewcart')

def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    # print(c)
    oid=random.randrange(1000,9999)
    # print(oid)
    for x in c:
        # print(x)   #object
        # print(x.pid, "=", x.uid, "-", x.qty)
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    context={}
    orders=Order.objects.filter(uid=request.user.id)
    np=len(orders) 
    context['data']=orders
    context['n']=np
    s=0
    for x in orders:
        s = s + x.pid.price * x.qty
    context['total']=s
    # return HttpResponse("Order Placed Successfully!!")
    return render(request,'placeorder.html',context)

def makepayment(request): 
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s = s + x.pid.price * x.qty
        oid=x.order_id

    client = razorpay.Client(auth=("rzp_test_nfTp8RVI8Ai3Ed", "0I6J9crsV7yTJikcZMYc4Jh1"))

    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    # print(payment)
    context={}
    context['data']=payment
    uemail=request.user.email
    print(uemail)
    context['uemail']=uemail
    # return HttpResponse("In makepayment function")
    return render(request,'pay.html',context)

def sendusermail(request,uemail):
    msg="Order details are:---"
    send_mail(
        "Ekart-Order placed successfully",
        msg,
        "rachana.rw19@gmail.com",   #owner email id
        [uemail], #user email id
        fail_silently=False,
)
    return HttpResponse("Mail sent successfully")

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')





