$(function () {

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
    // Create a supplier
    // ****************************************

    $("#create-btn").click(function () {

        var name = $("#supplier_name").val();
        var address = $("#supplier_address").val();
        var email = $("#supplier_email").val();
        var products = JSON.parse("[" + $("#supplier_products").val() + "]");

        var data = {
            "name": name,
            "address": address,
            "email": email,
            "products": products
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/api/suppliers",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a supplier
    // ****************************************

    $("#update-btn").click(function () {

        var name = $("#supplier_name").val();
        var address = $("#supplier_address").val();
        var email = $("#supplier_email").val();
        var products = JSON.parse("[" + $("#supplier_products").val() + "]");

        var data = {
            "name": name,
            "address": address,
            "email": email,
            "products": products
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/api/suppliers/" + supplier_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a supplier
    // ****************************************

    $("#retrieve-btn").click(function () {

        var supplier_id = $("#supplier_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/api/suppliers/" + supplier_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a supplier
    // ****************************************

    $("#delete-btn").click(function () {

        var supplier_id = $("#supplier_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/api/suppliers/" + supplier_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("supplier has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#supplier_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a supplier
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#supplier_name").val();
        var address = $("#supplier_address").val();
        var email = $("#supplier_email").val();
        var products = $("#supplier_products").val().trim();

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (address) {
            if (queryString.length > 0) {
                queryString += '&address=' + address
            } else {
                queryString += 'address=' + address
            }
        }
        if (email) {
            if (queryString.length > 0) {
                queryString += '&email=' + email
            } else {
                queryString += 'email=' + email
            }
        }
        if (products) {
            if (queryString.length > 0) {
                queryString += '&products=' + products
            } else {
                queryString += 'products=' + products
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/api/suppliers?" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Address</th>'
            header += '<th style="width:10%">Email</th></tr>'
            header += '<th style="width:10%">Products</th></tr>'
            $("#search_results").append(header);
            var firstSupplier = "";
            for(var i = 0; i < res.length; i++) {
                var supplier = res[i];
                var row = "<tr><td>"+supplier.id+"</td><td>"+supplier.name+"</td><td>"+supplier.address+"</td><td>"+supplier.email+"</td></tr>"+supplier.products+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstSupplier = supplier;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstSupplier != "") {
                update_form_data(firstSupplier)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
