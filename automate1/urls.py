from django.urls import path
from . import views

urlpatterns = [
    path("home", views.Index, name="home"),
    path("purchase", views.Purchase, name="purchase"),
    path("purchase/list", views.Purchase_list, name="purchase_list"),
    path("dashboard", views.Dashboard, name="dashboard"),
    path("login", views.Login, name="login"),
    path("product_list", views.Product_List, name="product_list"),
    path("product", views.Product_Form, name="product"),
    path("product_create", views.product_create, name="product_create"),
    path("sale", views.Sale, name="sale"),
    path("savepurchase", views.save_purchase, name="savepurchase"),
    path("purchase/update/<int:pk>/", views.Update_Purchase, name="update_purchase"),
    path("orders/<int:pk>/", views.order_view, name="order_view"),
    path("orders/delete/<int:pk>/", views.order_delete, name="order_delete"),
    path("supplier/list", views.Supplier_form, name="supplier_list"),
    path("supplier/", views.supplier_create, name="supplier_create"),
    path("vat/", views.vat_create, name="vat_create"),
    path("currency/", views.currency_create, name="currency_create"),
    path("credit-facility/", views.credit_facility_create, name="credit_facility_create"),
]
