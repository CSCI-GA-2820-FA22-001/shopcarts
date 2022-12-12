$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.customer_id);
        $("#shopcart_id").val(res.shopcart_id);
        $("#item_id").val(res.item_id);
        $("#item_name").val(res.item_name);
        $("#quantity").val(res.quantity);
        $("#price").val(res.price);
    }

    // Updates the form with data from the response (update shopcart_id)
    function update_form_data_for_create(res) {
        $("#shopcart_id").val(res.id);

    }

    /// Clears all form fields
    function clear_form_data() {
        $("#customer_id").val("");
        $("#shopcart_id").val("");
        $("#item_id").val("");
        $("#item_name").val("");
        $("#quantity").val("");
        $("#price").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }


    // ****************************************
    // Create Empty Shopcart
    // ****************************************

    $("#create-shopcart-btn").click(function () {

        let customer_id = Number($("#customer_id").val());

        let data = {
            "customer_id": customer_id,
            "items": []
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: `/shopcarts`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            update_form_data_for_create(res)
            $("#search_results").empty();
            $("#shopcarts_results").empty();
            flash_message("Successfully added an empty shopcart")
        });

        ajax.fail(function (res) {
            clear_form_data()
            $("#search_results").empty();
            $("#shopcarts_results").empty();
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Create Item
    // ****************************************

    $("#add-to-shopcart-btn").click(function () {

        let shopcart_id = parseInt($("#shopcart_id").val());
        let id = parseInt($("#item_id").val());
        let name = $("#item_name").val();
        let quantity = parseInt($("#quantity").val());
        let price = parseFloat($("#price").val());

        let data = {
            "id": id,
            "shopcart_id": shopcart_id,
            "name": name,
            "quantity": quantity,
            "price": price,
            "color": "blue"
        };

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "POST",
            url: `/shopcarts/${shopcart_id}/items`,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            clear_form_data()
            $("#search_results").empty();
            $("#shopcarts_results").empty();
            flash_message("Successfully added an Item")
        });

        ajax.fail(function (res) {
            clear_form_data()
            $("#search_results").empty();
            $("#shopcarts_results").empty();
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Retrieve Item
    // ****************************************
    $("#get-item-btn").click(function () {
        let shopcart_id = parseInt($("#shopcart_id").val());
        let item_id = parseInt($("#item_id").val());

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/${shopcart_id}/items/${item_id}`,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">Item ID</th>'
            table += '<th class="col-md-2">Item Name</th>'
            table += '<th class="col-md-2">Quantity</th>'
            table += '<th class="col-md-2">Price</th>'
            table += '<th class="col-md-2">Shopcart_ID</th>'
            table += '</tr></thead><tbody>'

            let item = res;
            table += `<tr><td>${item.id}</td><td>${item.name}</td><td>${item.quantity}</td><td>${item.price}</td><td>${item.shopcart_id}</td></tr>`;
            table += '</tbody></table>';

            $("#search_results").append(table);

            update_form_data(res);
            $("#shopcarts_results").empty();
            flash_message("Successfully retrieved the item")
        });

        ajax.fail(function (res) {
            clear_form_data()
            $("#search_results").empty();
            $("#shopcarts_results").empty();
            flash_message(res.responseJSON.message)
        });

    });



    // ****************************************
    // Update Item
    // ****************************************

    $("#update-item-btn").click(function () {

        let shopcart_id = parseInt($("#shopcart_id").val());
        let item_id = parseInt($("#item_id").val());
        let quantity = parseInt($("#quantity").val());
        let price = parseFloat($("#price").val());

        // alert($("#price").val())
        let data = {};
        if ($("#quantity").val() == "0") {
            data["quantity"] = 0;
        }
        else if (!isNaN(quantity)) {
            data["quantity"] = quantity;
        }
        else if ($("#quantity").val() != "") {
            data["quantity"] = $("#quantity").val()
        }
        if ($("#price").val() == "0") {
            data["price"] = 0.0;
        }
        else if (!isNaN(price)) {
            data["price"] = price;
        }
        else if ($("#price").val() != "") {
            data["price"] = $("#price").val()
        }
        // alert(data["price"])
        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "PUT",
            url: `/shopcarts/${shopcart_id}/items/${item_id}`,
            contentType: "application/json",
            data: JSON.stringify(data)
        })

        ajax.done(function (res) {
            $("#search_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-2">Item ID</th>'
            table += '<th class="col-md-2">Quantity</th>'
            table += '<th class="col-md-2">Price</th>'
            table += '<th class="col-md-2">Shopcart_ID</th>'
            table += '</tr></thead><tbody>'

            let item = res;
            table += `<tr><td>${item_id}</td><td>${data["quantity"]}</td><td>${data["price"]}</td><td>${shopcart_id}</td></tr>`;
            table += '</tbody></table>';

            $("#search_results").append(table);

            clear_form_data()
            $("#shopcarts_results").empty();
            flash_message(`Successfully updated the item`)
        });

        ajax.fail(function (res) {
            clear_form_data()
            $("#search_results").empty();
            $("#shopcarts_results").empty();
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve Shopcart
    // ****************************************

    $("#retrieve-btn").click(function () {

        let shopcart_id = Number($("#shopcart_id").val());

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts/${shopcart_id}`,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            $("#shopcarts_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-5">Result in form of CustomerID, Shopcart_ID, Items[]</th>'
            table += '</tr></thead><tbody class="scrollTbody">'

            table += `<tr><td>Customer ID = ${res.customer_id}</td><td>Shopcart ID = ${res.id}</td></tr>`;

            for (let i = 0; i < res['items'].length; i++) {
                table += `<tr><td>One of it's Item </td><td>${JSON.stringify(res['items'][i])}</td></tr>`;
            }
            if (res['items'].length == 0) {
                table += `<tr><td>It has an EMPTY Item</td></tr>`;
            }
            table += '</tbody></table>';
            $("#shopcarts_results").append(table);

            clear_form_data()
            $("#search_results").empty();
            flash_message("Successfully retrieved the shopcart")
        });

        ajax.fail(function (res) {
            clear_form_data()
            $("#search_results").empty();
            $("#shopcarts_results").empty();
            flash_message(res.responseJSON.message)
        });

    });
    // ****************************************
    // List All Shopcarts
    // ****************************************
    $("#list-all-shopcarts-btn").click(function () {

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts`,
            // contentType: "application/json",
            data: ''
        })
        ajax.done(function (res) {
            $("#shopcarts_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-5">Result in form of CustomerID, Shopcart_ID, Items[]</th>'
            table += '</tr></thead><tbody class="scrollTbody">'

            for (let i = 0; i < res['shopcarts'].length; i++) {
                // table += `<tr><td>Serial No.${i}</td></tr>`;
                table += `<tr id="row_${i}"><td>Customer_ID = ${res['shopcarts'][i].customer_id}</td><td>Shopcart_ID = ${res['shopcarts'][i].id}</td></tr>`;
                for (let j = 0; j < res['shopcarts'][i]['items'].length; j++) {
                    table += `<tr><td>One of it's Item </td><td>${JSON.stringify(res['shopcarts'][i]['items'][j])}</td></tr>`;
                }
                if (res['shopcarts'][i]['items'].length == 0) {
                    table += `<tr><td>It has an EMPTY Item</td></tr>`;
                }
            }
            if (res['shopcarts'].length == 0) {
                table += `<tr><td>No shopcarts in database</td></tr>`;
            }
            table += '</tbody></table>';
            $("#shopcarts_results").append(table);

            clear_form_data()
            $("#search_results").empty();
            flash_message("Successfully listed all the shopcarts")
        });

        ajax.fail(function (res) {
            clear_form_data()
            $("#search_results").empty();
            $("#shopcarts_results").empty();
            flash_message(res.responseJSON.message)
        });

    });
    // ****************************************
    // Delete an Item
    // ****************************************

    $("#remove-btn").click(function () {

        let shopcart_id = parseInt($("#shopcart_id").val());
        let item_id = parseInt($("#item_id").val());

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/shopcarts/${shopcart_id}/items/${item_id}`,
            contentType: "application/json",
            data: ''
        });

        ajax.done(function (res) {
            clear_form_data()
            $("#search_results").empty();
            $("#shopcarts_results").empty();
            flash_message("Successfully deleted an item")
        });

        ajax.fail(function (res) {
            clear_form_data()
            $("#search_results").empty();
            $("#shopcarts_results").empty();
            flash_message("Successfully deleted an item")
        });
    });

    // ****************************************
    // Clear Shopcart
    // ****************************************
    $("#clear-shopcart-btn").click(function () {

        let shopcart_id = Number($("#shopcart_id").val());

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "DELETE",
            url: `/shopcarts/${shopcart_id}`,
            contentType: "application/json",
        });

        ajax.done(function (res) {
            clear_form_data()
            $("#search_results").empty();
            $("#shopcarts_results").empty();
            flash_message("Successfully cleared the shopcart")
        });

        ajax.fail(function (res) {
            clear_form_data()
            $("#search_results").empty();
            $("#shopcarts_results").empty();
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Search for a Shopcart
    // ****************************************
    $("#search-shopcarts-btn").click(function () {

        let shopcart_id = $("#shopcart_id").val();
        let customer_id = $("#customer_id").val();

        let queryString = ""

        if (shopcart_id) {
            queryString += 'id=' + shopcart_id
        }
        if (customer_id) {
            if (queryString.length > 0) {
                queryString += '&customer_id=' + customer_id
            } else {
                queryString += 'customer_id=' + customer_id
            }
        }

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: `/shopcarts?${queryString}`,
            //contentType: "application/json",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#shopcarts_results").empty();
            let table = '<table class="table table-striped" cellpadding="10">'
            table += '<thead><tr>'
            table += '<th class="col-md-5">Result in form of CustomerID, Shopcart_ID, Items[]</th>'
            table += '</tr></thead><tbody class="scrollTbody">'

            for (let i = 0; i < res['shopcarts'].length; i++) {
                // table += `<tr><td>Serial No.${i}</td></tr>`;
                table += `<tr id="row_${i}"><td>Customer_ID = ${res['shopcarts'][i].customer_id}</td><td>Shopcart_ID = ${res['shopcarts'][i].id}</td></tr>`;
                for (let j = 0; j < res['shopcarts'][i]['items'].length; j++) {
                    table += `<tr><td>One of it's Item </td><td>${JSON.stringify(res['shopcarts'][i]['items'][j])}</td></tr>`;
                }
                if (res['shopcarts'][i]['items'].length == 0) {
                    table += `<tr><td>It has an EMPTY Item</td></tr>`;
                }
            }
            if (res['shopcarts'].length == 0) {
                table += `<tr><td>No shopcarts in database</td></tr>`;
            }
            table += '</tbody></table>';
            $("#shopcarts_results").append(table);

            clear_form_data()
            $("#search_results").empty();
            flash_message("Successfully listed all shopcarts")
        });

        ajax.fail(function (res) {
            clear_form_data()
            $("#search_results").empty();
            $("#shopcarts_results").empty();
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Clear the Form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#flash_message").empty();
        clear_form_data()
        $("#search_results").empty();
        $("#shopcarts_results").empty();
    });

})