Feature: The Supplier service back-end
    As a Supplier Manager
    I need a RESTful service
    So that I can keep track of all my suppliers

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Suppliers UI Screen" in the title

Scenario: Create a Supplier Happy Path
    When I visit the "Home Page"
    And I set the "Name" to "KeQing"
    And I set the "Address" to "LiYue"
    And I set the "Products" to "8,2"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Email" field should be empty
    And the "Address" field should be empty
    And the "Products" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "KeQing" in the "Name" field
    And I should see "LiYue" in the "Address" field
    And I should see "2, 8" in the "Products" field

Scenario: Delete a Supplier Happy Path
    Given the following suppliers
        | name       | email        | address | products |
        | Kiddo      | abc@mail.com |         | 2,7,1    |
    When I visit the "Home Page"
    And I set the "Name" to "Kiddo"
    And I press the "Search" button
    Then I should see "abc@mail.com" in the "Email" field
    When I press the "Delete" button
    Then I should see the message "supplier has been Deleted!"
    When I set the "Name" to "Kiddo"
    And I press the "Search" button
    Then I should see the message "404 Not Found"

Scenario: Update a Supplier Happy Path
    Given the following suppliers
        | name       | email        | address | products |
        | Kitty      | abc@mail.com |         | 2,7,1    |
    When I visit the "Home Page"
    And I set the "Name" to "Kitty"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "1, 2, 7" in the "Products" field
    When I set the "Address" to "UK"
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I set the "Products" to "2,1,7"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "UK" in the "Address" field
    And I should see "Kitty" in the "Name" field


Scenario: Search a Supplier by Attributes Happy Path
    Given the following suppliers
        | name       | email        | address | products |
        | Kitty      | abc@mail.com | UK      | 2,7,1    |
        | Tom        |              | UK      | 1        |
    When I visit the "Home Page"
    And I set the "address" to "UK"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Kitty" in the results
    And I should see "Tom" in the results
    When I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Email" field should be empty
    And the "Address" field should be empty
    And the "Products" field should be empty
    When I set the "Products" to "1"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Tom" in the results
    And I should not see "Kitty" in the results

Scenario: List all Suppliers Happy Path
    Given the following suppliers
        | name       | email        | address | products |
        | Hello      | xyz@mail.com | US      | 3,4      |
        | Kitty      | abc@mail.com | UK      | 2,7,1    |
        | Tom        |              | UK      | 1        |
    When I visit the "Home Page"
    And I press the "List" button
    Then I should see "Hello" in the results
    And I should see "Kitty" in the results
    And I should see "Tom" in the results

Scenario: Search a Supplier by ID Happy Path
    Given the following suppliers
        | name       | email        | address | products |
        | Kitty      | abc@mail.com | UK      | 2,7,1    |
    When I visit the "Home Page"
    And I set the "address" to "UK"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Kitty" in the results
    When I set the "Name" to "None"
    And I PRESS the "Retrieve" button
    Then I should see "Kitty" in the "Name" field

Scenario: Add Products to a Supplier Happy Path
    Given the following suppliers
        | name       | email        | address | products |
        | Hello      | xyz@mail.com | US      | 3,4      |
        | Kitty      | abc@mail.com | UK      | 2,7,1    |
        | Tom        |              | UK      | 1        |
    When I visit the "Home Page"
    And I set the "Name" to "Hello"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hello" in the "Name" field
    And I should see "xyz@mail.com" in the "Email" field
    And I should see "US" in the "Address" field
    And I should see "3, 4" in the "Products" field
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Email" field should be empty
    And the "Address" field should be empty
    And the "Products" field should be empty
    When I paste the "Id" field
    And I set the "Products" to "5,6"
    And I press the "AddProducts" button
    Then I should see the message "Success"
    And I should see "Hello" in the "Name" field
    And I should see "xyz@mail.com" in the "Email" field
    And I should see "US" in the "Address" field
    And I should see "3, 4, 5, 6" in the "Products" field
    
Scenario: Create a Supplier Sad Path
    When I visit the "Home Page"
    And I set the "Name" to "KeQing"
    And I press the "Create" button
    Then I should see the message "400 Bad Request"

Scenario: Delete a Supplier Sad Path
    Given the following suppliers
        | name       | email        | address | products |
        | Kitty      | abc@mail.com |         | 2,7,1    |
    When I visit the "Home Page"
    And I set the "ID" to "0"
    And I press the "Delete" button
    Then I should see the message "404 Not Found"

Scenario: Search Suppliers Sad Path
    Given the following suppliers
        | name       | email        | address | products |
        | Kitty      | abc@mail.com |         | 2,7,1    |
    When I visit the "Home Page"
    and I set the "Products" to "1,7"
    And I press the "Search" button
    Then I should see the message "404 Not Found"
    When I set the "ID" to "1"
    And I press the "Retrieve" button
    Then I should see the message "404 Not Found"

Scenario: Add Products to a Supplier Sad Path
    Given the following suppliers
        | name       | email        | address | products |
        | Hello      | xyz@mail.com | US      | 3,4      |
        | Kitty      | abc@mail.com | UK      | 2,7,1    |
        | Tom        |              | UK      | 1        |
    When I visit the "Home Page"
    And I set the "Name" to "Hello"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Hello" in the "Name" field
    And I should see "xyz@mail.com" in the "Email" field
    And I should see "US" in the "Address" field
    And I should see "3, 4" in the "Products" field
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Email" field should be empty
    And the "Address" field should be empty
    And the "Products" field should be empty
    When I paste the "Id" field
    And I set the "Products" to "4,5"
    And I press the "AddProducts" button
    Then I should see the message "Duplicated products"
