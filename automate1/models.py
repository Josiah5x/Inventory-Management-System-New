from django.db import models

# Create your models here.
class CommercialAccount(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=100, null=True, blank=True)
    quantity = models.CharField(max_length=100, null=True, blank=True)
    balance = models.CharField(max_length=100, null=True, blank=True)

class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


class Vat(models.Model):
    name = models.CharField(max_length=100, unique=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=10)      # NGN, USD
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CreditFacility(models.Model):
    name = models.CharField(max_length=100, unique=True)
    days = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_code = models.CharField(max_length=50, unique=True)

    product_name = models.CharField(max_length=255)
    secondary_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)

    PRODUCT_TYPES = (
        ("Goods", "Goods"),
        ("Service", "Service"),
    )

    types = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPES,
        default="Goods"
    )

    vat_category = models.ForeignKey(
        Vat,
        on_delete=models.PROTECT
    )

    unit = models.CharField(max_length=20)

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    selling_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="selling_products"
    )

    brand = models.CharField(max_length=100, blank=True)
    family = models.CharField(max_length=100, blank=True)
    sub_family = models.CharField(max_length=100, blank=True)
    shelf_no = models.CharField(max_length=50, blank=True)

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name="products"
    )

    supplier_item_code = models.CharField(max_length=100, blank=True)

    supplier_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    supplier_currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name="supplier_products"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["product_name"]

    def __str__(self):
        return f"{self.product_code} - {self.product_name}"
    

class OrderDocument(models.Model):
    doc_code = models.CharField(max_length=10)
    doc_year = models.CharField(max_length=4)
    doc_num = models.CharField(max_length=20)
    doc_date = models.CharField(max_length=20)
    supplier_name = models.CharField(max_length=255, blank=True)
    supplier_invoice = models.CharField(max_length=100, blank=True)
    currency = models.CharField(max_length=10, blank=True)
    credit_fercility = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    project = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doc_code}-{self.doc_year}-{self.doc_num}"

class OrderItem(models.Model):
    document = models.ForeignKey(OrderDocument, on_delete=models.CASCADE, related_name="items")
    product_code = models.CharField(max_length=255)
    product_description = models.TextField(blank=True)
    warehouse = models.CharField(max_length=255, blank=True)
    product_qty = models.DecimalField(max_digits=10, decimal_places=3)
    product_unit = models.CharField(max_length=10)
    product_price = models.DecimalField(max_digits=12, decimal_places=2)
    product_amount = models.DecimalField(max_digits=12, decimal_places=2)
    percentage_discount = models.DecimalField(max_digits=5, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2)
    gross_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.product_code

