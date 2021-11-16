$(function () {
    const baseUrl = "/api/suppliers";
    const contentType = "application/json"

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#supplier_id").val(res._id);
        $("#supplier_name").val(res.name);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#supplier_name").val("");
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

        let data = {
            "name": name,
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
            flash_message(res.responseJSON.error);
        });
    });


    // ****************************************
    // Update a Supplier 
    // ****************************************

    $("#update-btn").click(function () {

        let supplier_id = $("#supplier_id").val();
        let name = $("#supplier_name").val();

        let data = {
            "name": name,
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
            flash_message(res.responseJSON.error)
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
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.error)
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
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Supplier has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.error)
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
    // Search for a Supplier 
    // ****************************************

    $("#search-btn").click(function () {

        let name = $("#supplier_name").val();

        let queryString = ""

        if (name) {
            queryString += 'name=' + name
        }

        let ajax = $.ajax({
            type: "GET",
            url: `${baseUrl}?${queryString}`,
            contentType: contentType,
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            let header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            $("#search_results").append(header);
            let firstSupplier = "";
            for(let i = 0; i < res.length; i++) {
                let supplier = res[i];
                let row = "<tr><td>"+supplier._id+"</td><td>"+supplier.name+"</td></tr>";
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
            flash_message(res.responseJSON.error)
        });

    });

})
