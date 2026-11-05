from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Inventory, Sales
from .forms import RecordSaleForm, RegisterForm, LoginForm, IventoryForm, MakeSale, editForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import F, Sum
from django.utils import timezone


# Create your views here.
@login_required
def index(request):
    products = Inventory.objects.filter(is_active=True, owner = request.user).order_by("-created_at")
    ivform = IventoryForm()
    history = Sales.objects.filter(product__owner=request.user).order_by("-created_at")
    low_stock = Inventory.objects.filter(owner =request.user, is_active =True, quantity__lte=F("is_low_stock")).count()

    total_product = products.count()
    total_stocks= products.aggregate(total =Sum('quantity'))['total']or 0
    today = timezone.localdate()
    today_sales = Sales.objects.filter(product__owner=request.user, created_at__date=today)
    today_revenue = today_sales.aggregate(total=Sum(F("quantity") * F("price_per_item")) )["total"] or 0
    in_stock = Inventory.objects.filter(owner=request.user, is_active=True, quantity__gt=F("is_low_stock")).count()   
    out_of_stock = Inventory.objects.filter(owner=request.user, is_active=True, quantity=0).count()
    summary = products.aggregate(total_units=Sum('quantity'), inventory_value=Sum(F('quantity') * F('price')))
    recent_sales = history[:5]
    today_sales = today_sales.count()
   
    return render(request,
                   "stockup/index.html",
                     {"products": products, "ivform":ivform,
                       "history":history, "low_stock":low_stock,
                       "total_product":total_product, "total_stocks":total_stocks, 
                       "today_revenue":today_revenue, "today_sales":today_sales, "recent_sales": recent_sales, "in_stock": in_stock, "out_of_stock": out_of_stock, "summary": summary,
                       "total_units": summary['total_units'] or 0, "inventory_value": summary['inventory_value'] or 0 } )


@login_required
def NewIventory(request):
    if request.method == "POST":
        form = IventoryForm(request.POST)
        if form.is_valid():
            product= form.save(commit=False)
            product.owner = request.user
            product.save()
            return redirect("details", product_id=product.id)
    else:
        form = IventoryForm()
    return render(request, "stockup/create.html", {"form":form})    
          

@login_required
def IventoryDetails(request, product_id):
    product = get_object_or_404(Inventory, pk=product_id, owner=request.user)
    form1 = MakeSale()
    form2 = editForm(instance=product)
    sales = Sales.objects.filter(product=product).order_by("-created_at")[:5]
    low_stock = product.quantity <= product.is_low_stock
    


    return render(request,"stockup/details.html", {"product": product, "form1": form1, "form2": form2 , "sales":sales, "low_stock":low_stock} )

@require_POST
@login_required
def sale_view(request, product_id):
    product = get_object_or_404(Inventory, pk=product_id, is_active=True, owner=request.user)
    if request.method == "POST":
     
      form = MakeSale(request.POST)
      if form.is_valid():
          sale_quantity = form.cleaned_data['quantity']
          if sale_quantity > product.quantity:
              form.add_error('quantity', 'Not enough stock available')
              messages.warning(request, "Not enough stock available")
          else:
              with transaction.atomic():
                  sale = form.save(commit=False)
                  sale.product = product
                  sale.price_per_item = product.price
                  sale.save()  

                  product.quantity -= sale_quantity
                  product.save()
                  
                  
              return redirect('details', product_id = product.id) 
    else: 
        form = MakeSale()
    return render(request,"stockup/details.html", {"product": product, "form1": form} )
    
   
@require_POST
@login_required         
def editIventory(request, product_id):
    product = get_object_or_404(Inventory, pk=product_id, is_active=True, owner =request.user)
    if request.method == "POST":
        
        form = editForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('details', product_id=product.id)
    else:
        form= editForm(instance=product)
    return render(request,"stockup/details.html", {"product": product, "form2": form } )    
    
        
@login_required
def product_list(request):
    products = Inventory.objects.filter(
        owner=request.user,
        is_active=True
    ).order_by("-created_at")
    total_product = products.count()
    in_stock = Inventory.objects.filter(owner=request.user, is_active=True, quantity__gt=F("is_low_stock")).count()   
    out_of_stock = Inventory.objects.filter(owner=request.user, is_active=True, quantity=0).count()
    summary = products.aggregate(total_units=Sum('quantity'), inventory_value=Sum(F('quantity') * F('price')))
    low_stock = Inventory.objects.filter(owner =request.user, is_active =True, quantity__lte=F("is_low_stock")).count()
        

    return render(request, "stockup/products.html", {
        "products": products,
        "in_stock": in_stock,
        "out_of_stock": out_of_stock,
        "total_product": total_product,
        "total_stocks": summary['total_units'],
        "inventory_value": summary['inventory_value'],
        "low_stock": low_stock
    })                      
    

@require_POST
@login_required
def deleteIventory(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Inventory, pk=product_id, owner = request.user)
        product.is_active = False
        product.save()
        return redirect("index")



@login_required
def low_stockView(request):
    products = Inventory.objects.filter(owner=request.user, is_active=True, quantity__lte=F("is_low_stock")).order_by("-created_at")
    out_of_stock = products.filter(quantity=0).count()
    low_stock_count = products.filter(quantity__gt=0).count()
    
    return render(request, "stockup/lowstock.html", {"products": products, "out_of_stock": out_of_stock, "low_stock": low_stock_count, "total_low_stock": products.count()})
    


@login_required
def record_sale(request):
    if request.method == "POST":
        form = RecordSaleForm(request.POST, user=request.user)

        if form.is_valid():
            sale = form.save(commit=False)

            product = sale.product

            if sale.quantity > product.quantity:
                form.add_error(
                    "quantity",
                    f"Only {product.quantity} units are available."
                )
            else:
                sale.price_per_item = product.price
                sale.save()

                product.quantity -= sale.quantity
                product.save()

                return redirect("index")

    else:
        form = RecordSaleForm(user=request.user)
        products = form.fields["product"].queryset
        

    return render(
        request,
        "stockup/record_sale.html",
        {"form": form, "products": products}
    )





def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "stockup/register.html", {"form": form})    


def loginView(request):
    if request.method =="POST":
        form = LoginForm(request, data=request.POST)  
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)   
            return redirect("index")

    else:
        form = LoginForm(  )

    return render(request, "stockup/login.html", {"form": form})    



def logoutView(request):
    auth_logout(request)
    return redirect("login")