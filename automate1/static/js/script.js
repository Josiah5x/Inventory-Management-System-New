$(document).ready(function () {
  // ==========================
  // CSRF Helper
  // ==========================
  function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");

      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();

        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

          break;
        }
      }
    }

    return cookieValue;
  }

  // ==========================
  // Add Row
  // ==========================
  $("#add-row").click(function () {
    let newRow = `
       <tr>
                <td></td>

                <td>
                    <input type="text" class="form-control" name="product_code">
                </td>

                <td>
                    <input type="text" class="form-control" name="product_description">
                </td>

                <td>
                    <input type="text" class="form-control" name="warehouse" value="Kuje Store">
                </td>

                <td>
                    <input type="number" class="form-control" name="product_qty" value="1">
                </td>

                <td>
                    <select class="form-control" name="product_unit">
                        <option value=""></option>
                        <option>Pcs</option>
                        <option>Lits</option>
                        <option>SET</option>
                        <option>Gallons</option>
                        <option>Meters</option>
                    </select>
                </td>

                <td>
                    <input type="text" class="form-control" name="product_price">
                </td>

                <td>
                    <input type="text" class="form-control" name="product_amount" readonly>
                </td>

                <td>
                    <input type="text" class="form-control" name="percentage_discount">
                </td>

                <td>
                    <input type="text" class="form-control" name="discount" readonly>
                </td>

                <td>
                    <input type="text" class="form-control" name="gross_amount" readonly>
                </td>
            </tr>
        `;

    $("#table-body").append(newRow);
  });

  // Auto calculate whenever Qty, Price or Discount changes
  $(document).on(
    "input",
    "[name='product_qty'], [name='product_price'], [name='percentage_discount']",
    function () {
      let row = $(this).closest("tr");

      // Read values
      let qty = parseFloat(row.find("[name='product_qty']").val()) || 0;

      let price =
        parseFloat(
          row.find("[name='product_price']").val().replace(/,/g, "")
        ) || 0;

      let discountPercent =
        parseFloat(
          row.find("[name='percentage_discount']").val().replace("%", "")
        ) || 0;

      // Calculate Amount
      let amount = qty * price;

      // Calculate Discount
      let discount = (amount * discountPercent) / 100;

      // Calculate Gross
      let gross = amount - discount;

      // Update fields
      row.find("[name='product_amount']").val(amount.toFixed(2));
      row.find("[name='discount']").val(discount.toFixed(2));
      row.find("[name='gross_amount']").val(gross.toFixed(2));

      // Update Invoice Total
      calculateInvoiceTotal();
    }
  );

  function calculateInvoiceTotal() {
    let total = 0;

    $("#table-body tr").each(function () {
      let gross =
        parseFloat(
          $(this).find("[name='gross_amount']").val().replace(/,/g, "")
        ) || 0;

      total += gross;
    });

    $("#invoice_total").val(total.toFixed(2));
  }

  // ==========================
  // Load Products from Database
  // ==========================
  let products = [];

  fetch("/products/json/")
    .then((response) => response.json())
    .then((data) => {
      products = data;
      console.log("Products Loaded:", products);
    })
    .catch((error) => {
      console.error("Error loading products:", error);
    });

  // ==========================
  // Auto Fill Product Details
  // ==========================
  $(document).on("keyup change", "[name='product_code']", function () {
    let row = $(this).closest("tr");
    let value = $(this).val().trim().toLowerCase();

    if (value === "") {
      row.find("[name='product_description']").val("");
      row.find("[name='product_unit']").val("");
      row.find("[name='product_price']").val("");
      row.find("[name='product_amount']").val("");
      row.find("[name='discount']").val("");
      row.find("[name='gross_amount']").val("");
      calculateInvoiceTotal();
      return;
    }

    // Search by Product Code OR Product Name
    let product = products.find(
      (p) =>
        (p.product_code && p.product_code.toLowerCase() === value) ||
        (p.product_name && p.product_name.toLowerCase() === value)
    );

    if (product) {
      row.find("[name='product_code']").val(product.product_code);
      row
        .find("[name='product_description']")
        .val(product.description || product.product_name);
      row.find("[name='product_unit']").val(product.unit);
      row.find("[name='product_price']").val(product.price);

      // Recalculate automatically
      row.find("[name='product_qty']").trigger("input");
    }
  });

  // ==========================
  // Remove Row
  // ==========================
  $(document).on("click", ".remove-row", function () {
    $(this).closest("tr").remove();
  });

  // ==========================
  // Collect Items
  // ==========================
  function collectItems() {
    let items = [];

    $("#table-body tr").each(function () {
      let row = $(this);

      items.push({
        product_code: row.find('[name="product_code"]').val(),

        product_description: row.find('[name="product_description"]').val(),

        warehouse: row.find('[name="warehouse"]').val(),

        product_qty: row.find('[name="product_qty"]').val(),

        product_unit: row.find('[name="product_unit"]').val(),

        product_price: row.find('[name="product_price"]').val(),

        product_amount: row.find('[name="product_amount"]').val(),

        percentage_discount: row.find('[name="percentage_discount"]').val(),

        discount: row.find('[name="discount"]').val(),

        gross_amount: row.find('[name="gross_amount"]').val(),
      });
    });

    return items;
  }

  console.log($("#table-body").html());
  console.log($("#table-body tr").length);

  // ==========================
  // Build Parent Object
  // ==========================
  function buildPurchaseObject() {
    return {
      doc_code: $("#doc_code").val(),

      doc_year: $("#doc_year").val(),

      doc_num: $("#doc_num").val(),

      doc_date: $("#doc_date").val(),

      supplier_name: $("#supplier_select").val(),

      supplier_invoice: $("#supplier_invoice").val(),

      currency: $("#currency").val(),

      credit_fercility: $("#credit_fercility").val(),

      address: $("#supplier_address").val(),

      project: $("#project").val(),

      items: collectItems(),
    };
  }

  // ==========================
  // CREATE PURCHASE
  // ==========================
  $("#submitBtn").click(function (e) {
    e.preventDefault();

    let purchase = buildPurchaseObject();

    $.ajax({
      url: "/savepurchase/",

      type: "POST",

      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },

      contentType: "application/json",

      data: JSON.stringify(purchase),

      success: function (response) {
        alert(response.message);
      },

      error: function (xhr) {
        console.log(xhr.responseText);
      },
    });
  });

  // ==========================
  // UPDATE PURCHASE
  // ==========================
  $("#submitBtnUpdate").click(function (e) {
    e.preventDefault();

    let purchase = buildPurchaseObject();

    let id = $("#document_id").val();

    $.ajax({
      url: `/purchase/update/${id}/`,

      type: "POST",

      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },

      contentType: "application/json",

      data: JSON.stringify(purchase),

      success: function (response) {
        alert(response.message);
      },

      error: function (xhr) {
        console.log(xhr.responseText);
      },
    });
  });
});
