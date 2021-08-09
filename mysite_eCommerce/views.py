from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Product,Order,OrderItem , User, Customer, ShippingAddress
from django.contrib.auth import authenticate,login,logout
from .forms import CreateUserForm,Customerform,shippingform,edituserform
from django.views.decorators.csrf import csrf_exempt
from .task import emailsender


# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'mysite_eCommerce/Home.html', context)
def shopbybrand(request):
    brandprods = Product.objects.values('product_brand', 'id')
    l=[]
    brand = {item["product_brand"] for item in brandprods}
    for b in brand:
        prod = Product.objects.filter(product_brand=b)
        l.append([prod,len(prod)])
    context= {'products':l}
    return render(request,'mysite_eCommerce/brand.html', context)
def brandview(request, brand):
    print(brand)
    product = Product.objects.filter(product_brand=brand)
    context = {'brand':brand,"products":product}
    return render(request,'mysite_eCommerce/view.html',context)
def shopbycatagory(request):
    catprods = Product.objects.values('product_category', 'id')
    l = []
    cats = {item["product_category"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(product_category=cat)
        l.append([prod, len(prod)])
    context = {'products': l}
    return render(request, 'mysite_eCommerce/catg.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created =Order.objects.get_or_create(customer = customer , Completed = False)
        items = order.orderitem_set.all()
    else:
        return render(request, "mysite_eCommerce/login.html")
    context={'item':items , 'order':order}
    return render(request,"mysite_eCommerce/cart.html", context)

def productview(request,id):
    print(id)
    pview = Product.objects.get(id= id)
    otherproduct = Product.objects.filter(product_category = pview.product_category)
    context= {'pview':pview, 'products':otherproduct}
    return render(request,"mysite_eCommerce/productview.html", context)

def search(request):
    if request.method == "GET":
        sn=request.GET.get('search_name')
        if Product.objects.filter(product_category = sn).exists():
            QS = Product.objects.filter(product_category = sn)
        elif Product.objects.filter(product_name = sn).exists():
            QS = Product.objects.filter(product_name = sn)
        else:
            QS = "Record Not Found!!!"
        context = {'QS': QS}
        return render(request, "mysite_eCommerce/search.html", context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created =Order.objects.get_or_create(customer = customer , Completed = False)
        items = order.orderitem_set.all()
        c_user = request.user
        user = User.objects.get(id=c_user.id)
        form = edituserform(
            initial={'first_name': c_user.first_name, 'last_name': c_user.last_name, 'email': c_user.email})
        cobj = Customer.objects.get(user_id=c_user.id)
        cform = Customerform(initial={'mobile_no': cobj.mobile_no, 'alter_mobile': cobj.alter_mobile})
        sobj = ShippingAddress.objects.get(user_id=c_user.id)
        sform = shippingform(
            initial={'Addressline1': sobj.Addressline1, 'Addressline2': sobj.Addressline2, 'City': sobj.City,
                     'State': sobj.State, 'Zipcode': sobj.Zipcode, 'Country': sobj.Country})
        if request.method == "POST":
            print("Hello")
            cform = Customerform(request.POST, instance=cobj)
            sform = shippingform(request.POST, instance=sobj)
            print(cform.errors)
            print(sform.errors)
            if cform.is_valid() and sform.is_valid():
                cform.save()
                sform.save()
                message = f"Your Order is ready with info:"
                email_id = c_user.email
                for i in items:
                    pQuantity = Product.objects.get(product_name = i.product.product_name)
                    if pQuantity.product_quantity <= 0:
                        message += f"\n{pQuantity.product_name} is out of stoke."
                    else:
                        message +=f"\n{pQuantity.product_name} of total item {i.Quantity}"
                message += f"\nYour Order will be delivered ,With Shipping Address:\n City:{sobj.City}, Zipcode:{sobj.Zipcode}\n Address:{sobj.Addressline1},{sobj.Addressline2} \n You may like more PRoduct which are added recently .You can go to website and buy new items.\n Thankyou for Shopping!!!!"
                emailsender.delay(email_id, message)
                return redirect('Home')
            else:
                print("Error occured!!!")

    else:
        return render(request, "mysite_eCommerce/login.html")
    context={'item':items , 'order':order, 'cform':cform , 'form':form , 'sform':sform}
    return render(request,"mysite_eCommerce/Checkout.html", context)


def registrationpage(request):
    form = CreateUserForm()
    customerform = Customerform()
    shipform = shippingform()
    if request.method == "POST":
        print("Hello")
        form = CreateUserForm(request.POST)
        customerform = Customerform(request.POST)
        shipform = shippingform(request.POST)
        if form.is_valid() and customerform.is_valid() and shipform.is_valid():
            print("Here!!!!")
            form.save()
            un = form.cleaned_data['username']
            obj = User.objects.get(username = un)
            cust = Customer(mobile_no = customerform.cleaned_data['mobile_no'], user_id = obj, alter_mobile = customerform.cleaned_data['alter_mobile'])
            cust.save()
            shipadd = ShippingAddress(user_id = obj ,Addressline1=shipform.cleaned_data['Addressline1'], Addressline2=shipform.cleaned_data['Addressline2'],City =shipform.cleaned_data['City'] , State = shipform.cleaned_data['State'],Zipcode =shipform.cleaned_data['Zipcode'],Country=shipform.cleaned_data['Country'])
            shipadd.save()
            return render(request,"mysite_eCommerce/login.html")
        else:
            print("one form is not valid")
    context={'form':form, 'cform':customerform, 'sform':shipform}
    return render(request, "mysite_eCommerce/Signin.html", context)


def loginpage(request):
    if request.method =="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request ,username = username, password = password )
        if user is not None:
            login(request,user)
            return redirect('Home')


    context = {}
    return render(request, "mysite_eCommerce/login.html", context)


def logoutpage(request):
    logout(request)
    return redirect("Home")

def viewprofile(request):
    current_user = request.user
    cust_obj = Customer.objects.get(user_id = current_user.id)
    shadd_obj = ShippingAddress.objects.get(user_id = current_user.id)
    context = {'user':current_user, 'cobj':cust_obj, 'sobj':shadd_obj}
    return render(request,"mysite_eCommerce/viewprofile.html", context)

def editprofile(request):
    c_user = request.user
    user = User.objects.get(id = c_user.id)
    form = edituserform(initial={'first_name': c_user.first_name,'last_name':c_user.last_name, 'email':c_user.email})
    cobj = Customer.objects.get(user_id = c_user.id)
    cform = Customerform(initial={'mobile_no':cobj.mobile_no, 'alter_mobile':cobj.alter_mobile})
    sobj = ShippingAddress.objects.get(user_id = c_user.id)
    sform = shippingform(initial={'Addressline1':sobj.Addressline1,'Addressline2':sobj.Addressline2,'City':sobj.City,'State':sobj.State,'Zipcode':sobj.Zipcode,'Country':sobj.Country})
    if request.method == "POST":
        print("Hello")
        form = edituserform(request.POST,instance=user)
        cform = Customerform(request.POST,instance=cobj)
        sform = shippingform(request.POST,instance=sobj)
        print(form.errors)
        if  form.is_valid() and cform.is_valid() and sform.is_valid():
            form.save()
            cform.save()
            sform.save()
        else:
            print("Error occured!!!")

    context = {'form':form , 'cform':cform , 'sform':sform }
    return render(request,"mysite_eCommerce/editprofile.html",context)


@csrf_exempt
def updateItem(request):
    if request.method == "POST":
        pid = request.POST.get('pid')
        action = request.POST.get('action')
        print(pid,action)
        customer =request.user.customer
        product = Product.objects.get(id = pid)
        order, created = Order.objects.get_or_create(customer=customer, Completed=False)
        orderitem , created =OrderItem.objects.get_or_create(order =order, product =product)

        if action == "add":
            orderitem.Quantity= (orderitem.Quantity+1)
        elif action == "remove":
            orderitem.Quantity = (orderitem.Quantity - 1)

        orderitem.save()

        if orderitem.Quantity <=0:
            orderitem.delete()

    return JsonResponse('Item was Added',safe=False)



def test(request):

    cu = request.user
    context = {'cu':cu}
    return render(request, "mysite_eCommerce/test.html",context)