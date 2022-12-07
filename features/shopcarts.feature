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
        Then I should see "Shopcart REST API Service available at /shopcarts" in the title
        And I should not see "404 Not Found"