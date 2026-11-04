from django.urls import path

from . import views

urlpatterns =[
    path("", views.index, name = "index"),
    path("register/", views.register, name = "register"),
    path("login/", views.loginView, name = "login"),
    path("logout/", views.logoutView, name = "logout"),
    path("create/", views.NewIventory, name = "create"),
    path("details/<int:product_id>/", views.IventoryDetails, name = "details"),
    path("details/<int:product_id>/sale", views.sale_view, name = "sales"),
    path("details/<int:product_id>/edit", views.editIventory, name = "edit"),
    path("details/<int:product_id>/delete", views.deleteIventory, name = "delete"),
    path("lowstock/", views.low_stockView, name = "lowstock"),
    path("products/", views.product_list, name="products")
    
          

    
]