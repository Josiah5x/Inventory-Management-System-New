$(document).ready(function () {

    // Add row
    $("#add-row").click(function () {
        // var rowCount = $("#table-body tr").length + 1;
        var newRow = `
        <tr>
                <td><input class="form-check-input" type="checkbox" id="check1" name="option1" value="something" checked style="width: 25px; height: 25px"></td>
                <td><input type="text" class="form-control" name="product_code" value="4i4564 Cmp-Fuel Pump"></td>
                <td><input type="text" class="form-control" name="product_description"></td>
                <td><input type="text" class="form-control" value="Kuje Store" name="warehouse">
                </td>
                <td><input type="text" class="form-control" value="1.000" name="product_qty"></td>
                <td>
                    <select class="form-control" name="product_unit" id="product_unit"

                        <option value=""></option>
                        <option value="PC">PC</option>
                        <option value="LIT">LIT</option>
                        <option value="SET">SET</option>
                        <option value="GALLON">GALLON</option>
                        <option value="MTR">MTR</option>
                    </select>
                </td>
                <td><input type="text" class="form-control" name="product-rate" value="120,000.00">
                </td>
                <td><input type="text" class="form-control" name="product-rate"></td>
                <td><input type="text" class="form-control" name="percentage-discount" value="%0">
                </td>
                <td><input type="text" class="form-control" name="discount" value="120,000.00">
                </td>
                <td><input type="text" class="form-control" name="gross-amount" value="120,000.00">
                </td>
            </tr>`;
        $("#table-body").append(newRow);
        // updateRowNumbers();
    });

    // Remove row
    $(document).on("click", ".remove-row", function () {
        $(this).closest("tr").remove();
        // updateRowNumbers();
    });

    // Submit form
    $("#submitBtn").click(function (e) {
        var $btn = $(this);

        // 1. Show loader and disable button
        $btn.prop('disabled', true);
        $('#loader').show();
        $('#response-message').empty(); // Clear previous messages
        // $("#dataForm").submit(function (e) {
        e.preventDefault();


        var targetForm = $("#dataForm");

        // 1. Paste your raw string directly into this variable
        const rawData = targetForm.serialize();
        // 2. Run the parser function
        const structuredObject = parseRawData(rawData);

        // 3. View your clean object
        // console.log(structuredObject);



        // Helper function to extract Django's CSRF cookie value safely
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Check if this cookie string begins with the name we want
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        let url = 'savepurchase';
        $.ajax({
            url: url,
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Reads your cookie tokens perfectly
            },
            data: JSON.stringify(structuredObject), // Sends structured parent/child properties cleanly
            contentType: "application/json",
            success: function (response) {
                // Stringified because alert() cannot print objects directly
                alert("Data saved successfully! Message: " + response.message);
            },
            error: function (xhr, status, error) {
                alert("Error saving data: " + error);
            }
        });

    });

    // --- PARSER ENGINE CODE ---
    function parseRawData(queryString) {
        const params = new URLSearchParams(queryString);

        // Extract top-level document info
        const result = {
            doc_code: params.get("doc_code") || "",
            doc_year: params.get("doc_year") || "",
            doc_num: params.get("doc_num") || "",
            supplier_name: params.get("supplier_name") || "",
            supplier_invoice: params.get("supplier_invoice") || "",
            currency: params.get("currency") || "",
            credit_fercility: params.get("credit_f") || "",
            supplier_address: params.get("supplier_address") || "",
            project: params.get("project") || "",
            items: []
        };

        // Capture every duplicate key entry into arrays
        const productCodes = params.getAll("code");
        const productDescriptions = params.getAll("description");
        const productWarehouse = params.getAll("warehouse");
        const productQtys = params.getAll("qty");
        const productUnits = params.getAll("unit");
        const productPrice = params.getAll("unit-price").filter(val => val !== ""); // Ignores trailing blank updates
        const productAmount = params.getAll("amount");
        const discountPercentages = params.getAll("percentage-discount");
        const discounts = params.getAll("discount");
        const grossAmounts = params.getAll("gross-amount");

        // Loop through and map array columns to item objects
        for (let i = 0; i < productCodes.length; i++) {
            result.items.push({
                product_code: productCodes[i] || "",
                product_Description: productDescriptions[i] || "",
                product_warehouse: productWarehouse[i] || "",
                product_qty: parseFloat(productQtys[i]) || 0,
                product_unit: productUnits[i] || "",
                product_price: parseFloat(productPrice[i]?.replace(/,/g, "")) || 0,
                product_amount: parseFloat(productAmount[i]?.replace(/,/g, "")) || 0,
                percentage_discount: parseFloat(discountPercentages[i]?.replace("%", "")) || 0,
                discount: parseFloat(discounts[i]?.replace(/,/g, "")) || 0,
                gross_amount: parseFloat(grossAmounts[i]?.replace(/,/g, "")) || 0
            });
        }

        return result;
    }

});




