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
    path("invoice_temp", views.Invoice, name="invoice"),
    path("products/json/", views.product_json, name="product_json"),
    path("suppliers/json/", views.supplier_json, name="supplier_json"),
    path("currencies/json/", views.currency_json, name="currency_json"),
    path("facilities/json/", views.facility_json, name="facility_json"),
    path("savepurchase/", views.save_purchase, name="save_purchase"),
    path("purchase/update/<int:pk>/", views.Update_Purchase, name="update_purchase"),
    path("orders/<int:pk>/", views.order_view, name="order_view"),
    path("orders/delete/<int:pk>/", views.order_delete, name="order_delete"),
    path("supplier/list", views.Supplier_form, name="supplier_list"),
    path("supplier/", views.supplier_create, name="supplier_create"),
    path("vat/", views.vat_create, name="vat_create"),
    path("currency/", views.currency_create, name="currency_create"),
    path("credit-facility/", views.credit_facility_create, name="credit_facility_create"),
    # weasyprint
    path("invoice/<int:pk>/", views.render_invoice, name="invoice_view"),
    # playwright
    path("invoice/<int:pk>/", views.render_invoice2, name="invoice_view"),
]
