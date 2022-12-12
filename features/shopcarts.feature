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
        And I set the "customer_id" to "5566"
        And I set the "item_id" to "40"
        And I set the "item_name" to "Banana"
        And I set the "quantity" to "1"
        And I set the "price" to "0.5"
        And I set the "color" to "green"
        And I press the "create-shopcart-btn" button
        Then I should see the message "Success"
        When I copy the "shopcart_id" field
        And I press the "clear-btn" button
        Then the "shopcart_id" field should be empty
        And the "item_id" field should be empty
        And the "item_name" field should be empty
        And the "quantity" field should be empty
        And the "price" field should be empty
        And the "color" field should be empty
        When I paste the "ID" field

        And I should see "4" in the "shopcart_id" field

    Scenario: List all Shopcarts
        When I visit the "home page"
        # not there yet
        And I press the "List All Shopcarts" button
        Then I should see the message "Success"
        And I should see "1" in the results
        And I should see "2" in the results
        And I should see "3" in the results

    Scenario: Query a Shopcart
        When I visit the "home page"
        And I set the "customer_id" to "12"
        And I press the "search" button
        Then I should see the message "Success"
        And I should see "3" in the results

    Scenario: Checkout a Shopcart
        When I visit the "home page"
        And I set the "shopcart_id" to "1"
        # not there yet
        And I press the "checkout" button
        Then I should see the message "Success"
    # not done yet



    Scenario: Retrieve a Shopcart
        When I visit the "home page"
        And I set the "shopcart_id" to "1"
        And I press the "retrieve" button
        Then I should see the message "Success"
        And I should see "10" in the "customer_id" field
    # And I should see "[{'id':5, 'name':'MacBook', 'price':1000, 'quantity':1, 'color':'silver'}]" in "items"

    Scenario: Update a Shopcart
        When I visit the "home page"
        And I set the "shopcart_id" to "2"
        And I set the "customer_id" to "7788"
        Then I should see the message "Success"
        When I set the "shopcart_id" to "2"
        And I press the "retrieve" button
        Then I should see "7788" in the "customer_id" field

    Scenario: Delete a Shopcart
        When I visit the "home page"
        And I set the "shopcart_id" to "1"
        Then I should see the message "Success"
        And I should see "10" in the "customer_id" field
        When I set the "shopcart_id" to "1"
        And I press the "delete" button
        Then I should see the message "Shopcart has been Deleted!"
