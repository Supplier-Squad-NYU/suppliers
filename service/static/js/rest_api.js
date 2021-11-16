$(function () {
    const baseUrl = "/suppliers";
    const contentType = "application/json"

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
    // Create a supplier
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

        let supplier_id = $("#supplier_id").val();

        let ajax = $.ajax({
            type: "GET",
            url: `${baseUrl}/${supplier_id}`,
            contentType: contentType,
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

        let supplier_id = $("#supplier_id").val();

        let ajax = $.ajax({
            type: "DELETE",
            url: `${baseUrl}/${supplier_id}`,
            contentType: contentType,
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
        clear_form_data()
    });

    // ****************************************
    // Search for a supplier
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#supplier_name").val();
        let address = $("#supplier_address").val();
        let email = $("#supplier_email").val();
        let products = $("#supplier_products").val().trim();

        let queryString = ""

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

        let ajax = $.ajax({
            type: "GET",
            url: `${baseUrl}?${queryString}`,
            contentType: contentType,
            data: ''
        })

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
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
            let firstSupplier = ""
            for(let i = 0; i < res.length; i++) {
                let supplier = res[i];
                let row = "<tr><td>"+supplier.id+"</td><td>"+supplier.name+"</td><td>"+supplier.address+"</td><td>"+supplier.email+"</td></tr>"+supplier.products.map(String).join(", ")+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstSupplier = supplier
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form

            if (firstSupplier != "") {
                update_form_data(firstSupplier)
            }

            flash_message("Success")
        });
    });

})