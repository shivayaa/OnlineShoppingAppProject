from django.shortcuts import render,redirect,HttpResponse
from .models import User
from .forms import UserForm
from .models import Category,Product,Cart,Order 
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User 

# Create your views here.
cl=Category.objects.all()
pl=Product.objects.all()
def home(request):
    pl=Product.objects.all()
    d={'catlist':cl,'plist':pl}
    return render(request,'index.html',d) 

def addUser(request):
    if request.method=="POST":
        f=UserForm(request.POST)
        f.save()
        return redirect('/userLogin')
    else:
        f=UserForm
        d={'form':f,'catlist':cl}
        return render(request,'form.html',d) 

def userLogin(request):
    if request.method=="POST":
        uname=request.POST.get('uname')
        passw=request.POST.get('passw')
        usr=authenticate(request,username=uname,password=passw)
        if usr is not None:
            request.session['userName']=uname
            login(request,usr)
            return redirect('/')
        else:
            return HttpResponse('<h1> Invalid Username Or Password</h1>')
    else:   
        d={'catlist':cl}
        return render(request,'login.html',d) 

def userLogout(request):
    logout(request)
    return redirect('/')

def getProductByCategory(request):
    id=request.GET.get('id')
    pl=Product.objects.filter(category_id=id)
    d={'catlist':cl,'plist':pl}
    return render(request,'index.html',d)

def searchProduct(request):
    if request.method=="POST":
        pname=request.POST.get('sp')
        pl=Product.objects.filter(pname__icontains=pname)
        d={'catlist':cl,'plist':pl}
        return render(request,'searchProduct.html',d)
    else:
        pl=Product.objects.all()
        d={'catlist':cl,'plist':pl}
        return render(request,'searchProduct.html',d)

def productList(request):
    cl=Category.objects.all()
    pl=Product.objects.all()
    d={'catlist':cl,'plist':pl}
    return render(request,'productList.html',d)

def editProfile(request):
    userName=request.session.get('userName')
    usr=User.objects.get(username=userName)
    if request.method=='POST':
        f=UserForm(request.POST,instance=usr)
        f.save()
        return redirect('/')
    else:
        f=UserForm(instance=usr)
        d={'catlist':cl,'form':f}
        return render(request,'form.html',d) 

def addToCart(request):
    pid=request.GET.get('pid')
    prd=Product.objects.get(id=pid)
    userName=request.session.get('userName')
    usr=User.objects.get(username=userName)
    c=Cart()
    c.product=prd
    c.user=usr 
    c.save()
    return redirect('/')

def cartList(request):
    userName=request.session.get('userName')
    usr=User.objects.get(username=userName)

    # Order list delete function 
    if request.method == 'POST':
        totalBill=request.POST.get('bill')
        order=Order()
        order.totalBill=totalBill
        order.user=usr
        order.save()

        cartlist=Cart.objects.filter(user_id=usr.id)
        for i in cartlist:
            i.delete()
        return redirect('/myorder')
    

    else:
        cartlist=Cart.objects.filter(user_id=usr.id)
        totalbill=0
        for i in cartlist:
            totalbill=totalbill+i.product.price
        d={'catlist':cl,'cartlist':cartlist,'totalBill':totalbill}
        return render(request,'cartList.html',d)

def myorder(request):
    orlist=Order.objects.all()
    d={'catlist':cl,'orderlist':orlist}
    return render(request,'myorder.html',d)

from .models import MyImage
from .forms import MyImageForm
def imagedata(request):

    if request.method=="POST":
        f=MyImageForm(request.POST,request.FILES)
        f.save()
        f=MyImageForm
        imagelist=MyImage.objects.all()
        return render(request,'imageaccess.html',{'imagelist':imagelist,'form':f})
    else:
        f=MyImageForm
        imagelist=MyImage.objects.all()
        return render(request,'imageaccess.html',{'imagelist':imagelist,'form':f})








