from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
import json, traceback
from decimal import Decimal
from datetime import datetime
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.db import transaction
from .models import (
    OrderDocument,
    OrderItem,
    Supplier,
    Vat,
    Currency,
    CreditFacility,
    Product,
)


# Create your views here.
def Index(request):
    return render(request, "index.html")

def Purchase(request):
    # 1. Get the current date and time
    current_time = datetime.now()

    # 2. Extract just the year as an integer
    current_year = current_time.year
    suppliers = Supplier.objects.all()
    creditfacility = CreditFacility.objects.all()
    currencies = Currency.objects.all()
    context = {
        "suppliers": suppliers,
        "creditfacility": creditfacility,
        "currencies": currencies,
        "current_year":current_year,
    }
    return render(request, "purchase_invoice.html", context)

def Login(request):
    return render(request, "login.html")

def Dashboard(request):
    return render(request, "dashboard.html")

def Product_Form(request):
    suppliers = Supplier.objects.all()
    vats = Vat.objects.all()
    currencies = Currency.objects.all()
    context = {
        "suppliers": suppliers,
        "vats": vats,
        "currencies": currencies,
    }
    return render(request, "product_form2.html", context)

def Sale(request):
    return render(request, "sale.html")

def Invoice(request):
    return render(request, "invoice.html")

def Supplier_form(request):
    supplier = Supplier.objects.all()
    context = {"supplier": supplier}
    return render(request, "supplier_list.html", context)

def Purchase_list(request):
    # purchases = OrderDocument.objects.prefetch_related('items').all().order_by('-id')

    purchases = OrderDocument.objects.all()
    currencies = Currency.objects.all()
    suppliers = Supplier.objects.all()
    context = {
        "purchases": purchases,
        "currencies": currencies,
        "suppliers": suppliers,
    }

    return render(request, "purchase_list.html", context)
    # currencies = Currency.objects.all()
    # return render(request, "purchase_list.html", context)

def Product_List(request):
    products = Product.objects.all().order_by("-id")
    return render(request, "product_list.html", {"products": products})



def product_json(request):
    products = Product.objects.all()

    data = []

    for p in products:
        data.append({
            "id": p.id,
            "product_code": p.product_code,
            "product_name": p.product_name,
            "description": p.description,
            "unit": p.unit,
            "price": float(p.selling_price or 0),
        })

    return JsonResponse(data, safe=False)



def Update_Purchase(request, pk):
    if request.method == "GET":
        order = get_object_or_404(OrderDocument, pk=pk)
        order.currency = int(order.currency)
        order.credit_fercility = int(order.credit_fercility)
        order.supplier_name = int(order.supplier_name)
        current_time = datetime.now()

        # 2. Extract just the year as an integer
        current_year = current_time.year
        suppliers = Supplier.objects.all()
        creditfacility = CreditFacility.objects.all()
        currencies = Currency.objects.all()
        return render(
            request,
            "update_purchase.html",
            {
                "order": order,
                "orderitems": order.items.all(),   # All related OrderItems
                "suppliers": suppliers,
                "creditfacility": creditfacility,
                "currencies": currencies,
                "current_year":current_year,
                "order": order,
                "orderitems": order.items.all(),
            },
        )
        # Save the updated record
    elif request.method == "POST":
        data = json.loads(request.body)
        print(json.dumps(data))

    #     try:
    #         data = json.loads(request.body)
    #         print(json.dumps(data))

    #         with transaction.atomic():
    #             # Save parent matching your exact frontend keys
    #             document = OrderDocument.objects.create(
    #                 doc_code=data.get("doc_code"),
    #                 doc_year=data.get("doc_year"),
    #                 doc_num=data.get("doc_num"),
    #                 supplier_name=data.get("supplier_name"),
    #                 supplier_invoice=data.get("supplier_invoice"),
    #                 currency=data.get("currency"),
    #                 credit_fercility=data.get("credit_fercility"),
    #                 address=data.get("supplier_address"),
    #                 project=data.get("project"),
    #             )

    #             # Save the new parallel array values
    #             for item in data.get("items", []):
    #                 OrderItem.objects.create(
    #                     document=document,
    #                     product_code=item.get("product_code"),
    #                     product_description=item.get("product_Description"),
    #                     warehouse=item.get("product_warehouse"),
    #                     product_qty=item.get("product_qty"),
    #                     product_unit=item.get("product_unit"),
    #                     product_price=item.get("product_price"),
    #                     product_amount=item.get("product_amount"),
    #                     percentage_discount=item.get("percentage_discount"),
    #                     discount=item.get("discount"),
    #                     gross_amount=item.get("gross_amount"),
    #                 )

    #         return JsonResponse(
    #             {"status": "success", "message": "Data saved smoothly!"}, status=201
    #         )

    #     except Exception as e:
    #         return JsonResponse({"status": "error", "message": str(e)}, status=400)

    # return JsonResponse(
    #     {"status": "error", "message": "Method not allowed"}, status=405
    # )


def order_view(request, pk):
    order = get_object_or_404(OrderDocument, pk=pk)
    return render(request, "order_view.html", {"order": order})

def order_delete(request, pk):
    if request.method == "POST":
        order = get_object_or_404(OrderDocument, pk=pk)
        order.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "message": "Invalid request"})


# /////////////////////// SAVE SECTION ///////////////////////


def credit_facility_create(request):
    if request.method == "POST":
        CreditFacility.objects.create(name=request.POST.get("name"))
        messages.success(request, "Credit Facility saved successfully.")
        return redirect("credit_facility_create")
    return render(request, "creditfacility_form.html")



@transaction.atomic
def supplier_create(request):
    if request.method == "POST":
        try:
            Supplier.objects.create(
                name=request.POST.get("name"),
                address=request.POST.get("address"),
                phone=request.POST.get("phone"),
                email=request.POST.get("email"),
            )
            messages.success(request, "Supplier saved successfully.")
            return redirect("supplier_create")
        except Exception as e:
            messages.error(request, str(e))
    return render(request, "supplier_form.html")

def vat_create(request):
    if request.method == "POST":
        Vat.objects.create(name=request.POST.get("name"))
        messages.success(request, "VAT saved successfully.")
        return redirect("vat_create")
    return render(request, "vat_form.html")

def currency_create(request):
    if request.method == "POST":
        Currency.objects.create(name=request.POST.get("name"))
        messages.success(request, "Currency saved successfully.")
        return redirect("currency_create")
    return render(request, "currency_form.html")


def product_create(request):
    suppliers = Supplier.objects.all()
    vats = Vat.objects.all()
    currencies = Currency.objects.all()
    if request.method == "POST":
        Product.objects.create(
            product_code=request.POST.get("product_code"),
            product_name=request.POST.get("product_name"),
            secondary_name=request.POST.get("secondary_name"),
            description=request.POST.get("description"),
            types=request.POST.get("types"),
            vat_category=Vat.objects.get(id=request.POST.get("vat_category")),
            unit=request.POST.get("unit"),
            selling_price=request.POST.get("selling_price") or 0,
            selling_currency=Currency.objects.get(
                id=request.POST.get("selling_currency")
            ),
            brand=request.POST.get("brand"),
            family=request.POST.get("family"),
            sub_family=request.POST.get("sub_family"),
            shelf_no=request.POST.get("shelf_no"),
            supplier=Supplier.objects.get(id=request.POST.get("supplier")),
            supplier_item_code=request.POST.get("supplier_item_code"),
            supplier_price=request.POST.get("supplier_price") or 0,
            supplier_currency=Currency.objects.get(
                id=request.POST.get("supplier_currency")
            ),
        )
        messages.success(request, "Product saved successfully.")
        return redirect("product_create")
    context = {
        "suppliers": suppliers,
        "vats": vats,
        "currencies": currencies,
    }
    return render(request, "product_form2.html", context)


def to_decimal(value):
    if value in (None, "", " "):
        return Decimal("0")
    return Decimal(str(value).replace(",", ""))

@ensure_csrf_cookie
def save_purchase(request):
    print("POST Data:", request.body)
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            with transaction.atomic():
                # Save parent matching your exact frontend keys
                document = OrderDocument.objects.create(
                    doc_code=data.get("doc_code"),
                    doc_year=data.get("doc_year"),
                    doc_num=data.get("doc_num"),
                    doc_date=data.get("doc_date"),
                    supplier_name=data.get("supplier_name"),
                    supplier_invoice=data.get("supplier_invoice"),
                    currency=data.get("currency"),
                    credit_fercility=data.get("credit_fercility"),
                    address=data.get("address"),
                    project=data.get("project"),
                )

                # Save the new parallel array values
                for item in data.get("items", []):
                    OrderItem.objects.create(
                        document=document,
                        product_code=item.get("product_code"),
                        product_description=item.get("product_description"),
                        warehouse=item.get("warehouse"),
                        product_qty=item.get("product_qty"),
                        product_unit=item.get("product_unit"),
                        product_price=to_decimal(item.get("product_price")),
                        product_amount=to_decimal(item.get("product_amount")),
                        percentage_discount=to_decimal(item.get("percentage_discount")),
                        discount=to_decimal(item.get("discount")),
                        gross_amount=to_decimal(item.get("gross_amount")),
                    )

            return JsonResponse(
                {"status": "success", "message": "Data saved smoothly!"}, status=201
            )

        except Exception as e:
            traceback.print_exc()
            print("ERROR:", e)

            return JsonResponse({"status": "error","message": str(e)}, status=400)

    return JsonResponse(
        {"status": "error", "message": "Method not allowed"}, status=405
    )