# suppliers

[![Build Status](https://github.com/Supplier-Squad-NYU/suppliers/actions/workflows/python.yml/badge.svg)](https://github.com/Supplier-Squad-NYU/suppliers/actions/workflows/python.yml)

[![codecov](https://codecov.io/gh/Supplier-Squad-NYU/suppliers/branch/main/graph/badge.svg?token=AD8XDW91AM)](https://codecov.io/gh/Supplier-Squad-NYU/suppliers)

## Project Name
the Supplier Module of a E-commerce Program

## Project Function
This project is designed to store the information of Vendors that the commerce program gets suppliers from.
The information stored inside includes the id, name, email address of each supplier and the suppliers that supplier provides.
This project offers a convenient user interface on inserting, modifying, deleting, or finding the desire supplier with specific id, name, email address or list all the available suppliers in the database.
This project also provides a microservice for insertion, deletion, modification or searching.

## Finished Job
In Sprint 1, we developed a local RESTful service that is able to insert, delete, modify, and search a specific supplier.
In the local RESTful service, we used a dictionary to simulate our database. All the operations were targeted on this dictionary.
In the local service, inputs are accepted by HTTP GET, PUT, POST, and DELETE APIs and outputs are in JSON format.

In Sprint 2, we started to use a PostgreSQL database system and all the local service built in last Sprint was refactored to work with the new database.
Also, the supplier microservice was deployed to IBM cloud.
We also integrated our application to CI/CD pipeline using Github Actions.

In Sprint 3, we finished the job of Integrate CI/CD pipeline left in last Sprint.
Also, we Created a simple single page UI for our application.
We alsoe created BDD, and, wrote 7 senarios Create, Read, Update, Delete, List, Query, and Action.
We wrote  the feature using Gherkin syntax that is understood by the behave tool.

In Sprint 4, we refactored the micro service using swagger.
We also added Swagger annotations to the service to document our REST API and added Swagger data models to document the API payloads.

## Setting up the development environment
Install [Git](http://git-scm.com/downloads) for using bash commands.
To setup the development environment, we use [Vagrant](https://www.vagrantup.com/downloads) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads). The recommended code editor is [Visual Studio Code](https://code.visualstudio.com/).

The Vagrantfile installs all of the needed software to run the service. You can clone this github repository and follow the given commands to start running the service:

```bash
git clone https://github.com/Supplier-Squad-NYU/suppliers.git

cd suppliers    

#bring up the vm
vagrant up 

#open a shell inside the vm
vagrant ssh 

cd /vagrant

python3 run.py

[---------------------------------------------------------
    To display the logs use the following command instead:
    honcho start
---------------------------------------------------------]

#To run in debug mode
make debug

#To run tests
nosetests

#At this point the website will be live

#exit out of the vm shell back to your host computer
exit 

#shutdown the vm to return later with vagrant up
vagrant halt 
```

search [127.0.0.1:5000](http://127.0.0.1:5000/) on browser to access the website and find the URL for accessing '/suppliers' page.

### Prod Service Link
https://nyu-supplier-service-fall2101-prod.us-south.cf.appdomain.cloud/

### Swagger Documents Link
https://nyu-supplier-service-fall2101-prod.us-south.cf.appdomain.cloud/apidocs

### API Documentation

 |                 URL                 | HTTP Method |                         Description                          | HTTP Return Code |
| :---------------------------------: | :---------: | :----------------------------------------------------------: | :---------------:|
|              /suppliers              |   **GET**   |              Returns a list all of the suppliers              | HTTP_200_OK |
|           /suppliers/{id}            |   **GET**   |             Returns the supplier with a given id in JSON format             | HTTP_200_OK |
|              /suppliers              |  **POST**   | creates a new supplier with ID and creation date auto assigned by the Database and adds it to the suppliers list | HTTP_201_CREATED |
|           /suppliers/{id}            |   **PUT**   | updates the supplier with given id with the credentials specified in the request |  HTTP_200_OK |
|           /suppliers/{id}            | **DELETE**  |           deletes a supplier record from the database           | HTTP_204_NO_CONTENT |
|           /suppliers/{id}/products          | **POST**  |           add a new product to a existed supplier           | HTTP_200_OK |


### Testing
Use the following commands to run the test cases:

Mac: 
```
nosetests
```
Windows: 
```
nosetests --exe
```
