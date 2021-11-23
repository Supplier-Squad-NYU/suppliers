$(function () {
    const baseUrl = "/api/suppliers";
    const contentType = "application/json";

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#supplier_id").val(res.id);
        $("#supplier_name").val(res.name);
        $("#supplier_address").val(res.address);
        $("#supplier_email").val(res.email);
        $("#supplier_products").val(res.products.map(String).join(", "));
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#supplier_id").val("");
        $("#supplier_name").val("");
        $("#supplier_address").val("");
        $("#supplier_email").val("");
        $("#supplier_products").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Supplier
    // ****************************************

    $("#create-btn").click(function () {
        let name = $("#supplier_name").val();
        let address = $("#supplier_address").val();
        let email = $("#supplier_email").val();
        let products = JSON.parse("[" + $("#supplier_products").val() + "]");

        let data = {
            "name": name,
            "address": address,
            "email": email,
            "products": products
        };

        let ajax = $.ajax({
            type: "POST",
            url: baseUrl,
            contentType: contentType,
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.error);
        });
    });


    // ****************************************
    // Update a Supplier
    // ****************************************

    $("#update-btn").click(function () {
        let supplier_id = $("#supplier_id").val();
        let name = $("#supplier_name").val();
        let address = $("#supplier_address").val();
        let email = $("#supplier_email").val();
        let products = JSON.parse("[" + $("#supplier_products").val() + "]");

        let data = {
            "name": name,
            "address": address,
            "email": email,
            "products": products
        };

        let ajax = $.ajax({
                type: "PUT",
                url: `${baseUrl}/${supplier_id}`,
                contentType: contentType,
                data: JSON.stringify(data)
            });

        ajax.done(function(res){
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.error);
        });

    });

    // ****************************************
    // Retrieve a Supplier
    // ****************************************

    $("#retrieve-btn").click(function () {

        let supplier_id = $("#supplier_id").val();

        let ajax = $.ajax({
            type: "GET",
            url: `${baseUrl}/${supplier_id}`,
            contentType: contentType,
            data: ''
        });

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res){
            clear_form_data();
            flash_message(res.responseJSON.error);
        });

    });

    // ****************************************
    // Delete a Supplier
    // ****************************************

    $("#delete-btn").click(function () {

        let supplier_id = $("#supplier_id").val();

        let ajax = $.ajax({
            type: "DELETE",
            url: `${baseUrl}/${supplier_id}`,
            contentType: contentType,
            data: '',
        });

        ajax.done(function(res){
            clear_form_data();
            flash_message("supplier has been Deleted!");
        });

        ajax.fail(function(res){
            flash_message("404 Not Found");
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        clear_form_data();
    });

    // ****************************************
    // Search for a Supplier
    // ****************************************

    $("#search-btn").click(function () {

        let name = 'name='+$("#supplier_name").val();
        let address = 'address='+$("#supplier_address").val();
        let email = 'email='+$("#supplier_email").val();
        let products = 'products='+$("#supplier_products").val().trim();

        let queryString = [name, address, email, products].filter(keyword => keyword[keyword.length-1] !== "=").join('&');

        let ajax = $.ajax({
            type: "GET",
            url: `${baseUrl}?${queryString}`,
            contentType: contentType,
            data: ''
        });

        ajax.fail(function(res){
            clear_form_data();
            $("#search_results").empty();
            flash_message(res.responseJSON.error);
        });

        ajax.done(function(res){
            // alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="20">');
            let header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:10%">Name</th>'
            header += '<th style="width:10%">Address</th>'
            header += '<th style="width:10%">Email</th></tr>'
            header += '<th style="width:10%">Products</th></tr>'
            $("#search_results").append(header);
            let firstSupplier = "";
            for(let i = 0; i < res.length; i++) {
                let supplier = res[i];
                let row = "<tr><td>"+supplier.id+"</td><td>"+supplier.name+"</td><td>"+supplier.address+"</td><td>"+supplier.email+"</td></tr>"+supplier.products.map(String).join(", ")+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstSupplier = supplier;
                }
            };

            $("#search_results").append('</table>');

            // copy the first result to the form

            if (firstSupplier != "") {
                update_form_data(firstSupplier);
            }

            flash_message("Success");
        });
    });

    // ****************************************
    // List all Suppliers
    // ****************************************

    $("#list-btn").click(function () {

        let ajax = $.ajax({
            type: "GET",
            url: `${baseUrl}`,
            contentType: contentType,
            data: ''
        });

        ajax.fail(function(res){
            clear_form_data();
            $("#search_results").empty();
            flash_message(res.responseJSON.error);
        });

        ajax.done(function(res){
            // alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="20">');
            let header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:10%">Name</th>'
            header += '<th style="width:10%">Address</th>'
            header += '<th style="width:10%">Email</th></tr>'
            header += '<th style="width:10%">Products</th></tr>'
            $("#search_results").append(header);
            let firstSupplier = "";
            for(let i = 0; i < res.length; i++) {
                let supplier = res[i];
                let row = "<tr><td>"+supplier.id+"</td><td>"+supplier.name+"</td><td>"+supplier.address+"</td><td>"+supplier.email+"</td></tr>"+supplier.products.map(String).join(", ")+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstSupplier = supplier;
                }
            };

            $("#search_results").append('</table>');

            // copy the first result to the form

            if (firstSupplier != "") {
                update_form_data(firstSupplier);
            }

            flash_message("Success");
        });
    });

    // ****************************************
    // Add Products for a Supplier
    // ****************************************

    $("#add_products-btn").click(function () {

        let supplier_id = $("#supplier_id").val();
        let products = JSON.parse("[" + $("#supplier_products").val() + "]");
        let data = {
            "products": products
        }

        let ajax = $.ajax({
            type: "POST",
            url: `${baseUrl}/${supplier_id}/products`,
            contentType: contentType,
            data: JSON.stringify(data)
        });

        ajax.done(function(res){
            update_form_data(res);
            flash_message("Success");
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.error);
        });
    });

})
