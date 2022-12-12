Feature: The shopcart service back-end
    As a Shopcarts Admin
    I need a RESTful catalog service
    So that I can keep track of all my shopcarts

    Background:
        Given the following shopcarts
            | id | customer_id | items                                                                      |
            | 1  | 10          | [{'id':5, 'name':'MacBook', 'price':1000, 'quantity':1, 'color':'silver'}] |
            | 2  | 11          | [{'id':6, 'name':'Backpack', 'price':50, 'quantity':3, 'color':'black'}]   |
            | 3  | 12          | [{'id':7, 'name':'Sneaker', 'price':80, 'quantity':1, 'color':'yellow'}]   |

    Scenario: The server is running
        When I visit the "home page"
        Then I should see "Shopcart RESTful Service" in the title
        And I should not see "404 Not Found"

    Scenario: Create a Shopcart
        When I visit the "home page"
        And I set the "Customer ID" to "5566"
        And I press the "Create Shopcart" button
        Then I should see the message "Success"
        When I copy the "Shopcart ID" field
        And I press the "Clear Form" button
        Then the "Shopcart ID" field should be empty
        And the "Customer ID" field should be empty
        When I paste the "Shopcart ID" field
        And I press the "Retrieve Shopcart" button
        Then I should see the message "Success"
        And I should see "Customer ID = 5566" in the shopcart results
        And I should see "It has an EMPTY Item" in the shopcart results

    Scenario: List all Shopcarts
        When I visit the "home page"
        And I press the "List All Shopcarts" button
        Then I should see the message "Success"
        And I should see "Customer ID = 10" in the shopcart results
        And I should see "Item #1" in the shopcart results
        And I should see "color: silver" in the shopcart results
        And I should see "id: 5" in the shopcart results
        And I should see "name: MacBook" in the shopcart results
        And I should see "price: 1000" in the shopcart results
        And I should see "quantity: 1" in the shopcart results
        And I should see "Customer ID = 11" in the shopcart results
        And I should see "Item #1" in the shopcart results
        And I should see "color: black" in the shopcart results
        And I should see "id: 6" in the shopcart results
        And I should see "name: Backpack" in the shopcart results
        And I should see "price: 50" in the shopcart results
        And I should see "quantity: 3" in the shopcart results
        And I should see "Customer ID = 12" in the shopcart results
        And I should see "Item #1" in the shopcart results
        And I should see "color: yellow" in the shopcart results
        And I should see "id: 7" in the shopcart results
        And I should see "name: Sneaker" in the shopcart results
        And I should see "price: 80" in the shopcart results
        And I should see "quantity: 1" in the shopcart results

    Scenario: Search a Shopcart
        When I visit the "home page"
        And I set the "Customer ID" to "5566"
        And I press the "Create Shopcart" button
        Then I should see the message "Success"
        When I press the "Clear Form" button
        Then the "Shopcart ID" field should be empty
        And the "Customer ID" field should be empty
        When I set the "Customer ID" to "5566"
        And I press the "Search Shopcart" button
        Then I should see the message "Success"
        And I should see "Customer ID = 5566" in the shopcart results
        And I should see "It has an EMPTY Item" in the shopcart results

    Scenario: Retrieve a Shopcart
        When I visit the "home page"
        And I set the "Customer ID" to "10"
        And I press the "Search Shopcart" button
        Then I should see the message "Success"
        When I copy the "Shopcart ID" field
        And I press the "Clear Form" button
        Then the "Shopcart ID" field should be empty
        And the "Customer ID" field should be empty
        When I paste the "Shopcart ID" field
        And I press the "Retrieve Shopcart" button
        Then I should see the message "Success"
        And I should see "Customer ID = 10" in the shopcart results
        And I should see "Item #1" in the shopcart results
        And I should see "color: silver" in the shopcart results
        And I should see "id: 5" in the shopcart results
        And I should see "name: MacBook" in the shopcart results
        And I should see "price: 1000" in the shopcart results
        And I should see "quantity: 1" in the shopcart results

    Scenario: Delete a Shopcart
        When I visit the "home page"
        And I set the "Customer ID" to "5566"
        And I press the "Create Shopcart" button
        Then I should see the message "Success"
        When I copy the "Shopcart ID" field
        And I press the "Clear Form" button
        Then the "Shopcart ID" field should be empty
        And the "Customer ID" field should be empty
        When I paste the "Shopcart ID" field
        And I press the "Delete Shopcart" button
        Then I should see the message "Successfully cleared the shopcart"
        When I press the "List All Shopcarts" button
        Then I should not see "Customer ID = 5566" in the shopcart results
        And I should not see "It has an EMPTY Item" in the shopcart results

    Scenario: Add an Item to a Shopcart
        When I visit the "home page"
        And I set the "Customer ID" to "10"
        And I press the "Search Shopcart" button
        Then I should see the message "Success"
        When I copy the "Shopcart ID" field
        And I press the "Clear Form" button
        Then the "Shopcart ID" field should be empty
        And the "Customer ID" field should be empty
        When I paste the "Shopcart ID" field
        And I set the "Item ID" to "8"
        And I set the "Item Name" to "Banana"
        And I set the "Quantity" to "5"
        And I set the "Price" to "2.99"
        And I set the "Color" to "green"
        And I press the "Add to Shopcart" button
        Then I should see the message "Success"
        When I set the "Customer ID" to "10"
        And I press the "Search Shopcart" button
        Then I should see the message "Success"
        When I copy the "Shopcart ID" field
        And I press the "Clear Form" button
        And I paste the "Shopcart ID" field
        And I press the "Retrieve Shopcart" button
        Then I should see the message "Success"
        And I should see "Customer ID = 10" in the shopcart results
        And I should see "color: green" in the shopcart results
        And I should see "id: 8" in the shopcart results
        And I should see "name: Banana" in the shopcart results
        And I should see "price: 2.99" in the shopcart results
        And I should see "quantity: 5" in the shopcart results

    Scenario: Delete an Item from a Shopcart
        When I visit the "home page"
        And I set the "Customer ID" to "10"
        And I press the "Search Shopcart" button
        Then I should see the message "Success"
        When I copy the "Shopcart ID" field
        And I press the "Clear Form" button
        Then the "Shopcart ID" field should be empty
        And the "Customer ID" field should be empty
        When I paste the "Shopcart ID" field
        And I set the "Item ID" to "5"
        And I press the "Delete Item" button
        Then I should see the message "Success"
        When I set the "Customer ID" to "10"
        And I press the "Search Shopcart" button
        Then I should see the message "Success"
        And I should not see "color: silver" in the shopcart results
        And I should not see "id: 5" in the shopcart results
        And I should not see "name: MacBook" in the shopcart results
        And I should not see "price: 1000" in the shopcart results
        And I should not see "quantity: 1" in the shopcart results

    Scenario: Update an Item from a Shopcart
        When I visit the "home page"
        And I set the "Customer ID" to "10"
        And I press the "Search Shopcart" button
        Then I should see the message "Success"
        When I copy the "Shopcart ID" field
        And I press the "Clear Form" button
        Then the "Shopcart ID" field should be empty
        And the "Customer ID" field should be empty
        When I paste the "Shopcart ID" field
        And I set the "Item ID" to "5"
        And I set the "Quantity" to "2"
        And I set the "Color" to "Grey"
        And I set the "Price" to "2000"
        And I press the "Update Item" button
        Then I should see the message "Success"
        When I set the "Customer ID" to "10"
        And I press the "Search Shopcart" button
        Then I should see the message "Success"
        And I should see "color: Grey" in the shopcart results
        And I should see "price: 2000" in the shopcart results
        And I should see "quantity: 2" in the shopcart results
        And I should not see "color: silver" in the shopcart results
        And I should not see "price: 1000" in the shopcart results
        And I should not see "quantity: 1" in the shopcart results


# not done yet
#Scenario: Update a Shopcart
#    When I visit the "home page"
#    And I set the "shopcart_id" to "2"
#    And I set the "customer_id" to "7788"
#    Then I should see the message "Success"
#    When I set the "shopcart_id" to "2"
#    And I press the "retrieve" button
#    Then I should see "7788" in the "customer_id" field

#Scenario: Checkout a Shopcart
#    When I visit the "home page"
#    And I set the "shopcart_id" to "1"
#    # not there yet
#    And I press the "checkout" button
#    Then I should see the message "Success"
# not done yet



