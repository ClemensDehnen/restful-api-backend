# restful-api-backend
The project consists in the development of an database API. The API follows RESTful principles and delivers typical CRUD operations on the database sample data given in _data.json_

The sample data consists of 1000 items with the attributes:
-   status
-   price
-   start_date
-   end_date
-   city
-   color
-   id


## Technologies

The following technologies have been used:

- **Python** an universal interpreted programming language.
- **FastAPI** a simple to use Python web framework supporting data validation.
- **Pytest** a Python test framework which makes it easy to write and run unit and integration
tests.
- **Docker** container platform used to quickly, easily and reliably applications.

## API Endpoints

This API implements the following routes:

| **Endpoint**     	    | **HTTP method**   | **CRUD method** 	| **Description**      	|
|-----------------	    |----------------  	|---------------	|----------------------	|
| `/entry`     	        | POST        	    | INSERT      	    | add a new entry    	|
| `/entries`     	    | GET           	| READ        	    | get all entries    	|
| `/entries/max_id`     | GET           	| READ        	    | get the max id value  |
| `/entry/<entry_id>`   | GET         	    | READ        	    | get entry by id    	|
| `/entry/<entry_id>`   | PUT         	    | UPDATE      	    | update an entry by id |
| `/entry/<entry_id>`	| DELETE      	    | DELETE      	    | delete an entry by id |

A more complete documentation of the API is available at http://localhost:8080/docs after running the containers.

## Build the API image

To build, test and run this API we'll be using `docker-compose`. As such, the first step
is to build the images defined in the `docker-compose.yml` file.

```bash
$ docker-compose build
```

This will build two images:

- `api_backend` main image containing the REST API.
- `mongo_seeder` minimal mongodb image used to import the data.json seed into the mongodb.


## Run the Containers
 
To run the containers previously built, execute the following:
 
```bash
$ docker-compose up -d
```

This will launch three services named `api_backend` (the API), `mongo_db` (the database) and `mongo_seeder` (the seed importer) in daemon mode (without constant output). The `api_backend` service will then be available on port `8080` on localhost. The `mongo_seeder` will shutoff as soon as the test_data is imported into the `mongo_db`.
Docker-compose will also setup an interal network called `restful-api-backend_default` with an integrated DNS server and automatically registers all services on this network. The services are then able to reach eachother using their service names.

The API is protected using a Basic Authentication. To use the API u need to use the 

username **`cdehnen`**

and

password **`hireme`**


## Run the Tests

The tests can be executed with:

```bash
$ docker-compose exec api_backend pytest ./api_backend
```

Or including a coverage check:

```bash
$ docker-compose exec api_backend pytest ./api_backend --cov="."
```

## Check for Code Quality

Another step to ensure the code contains the desired quality is to perform *linting*, that 
is, to check for stylistic or programming errors. The following command will run the 
`pylint` linter throughout the source code:

```bash
$ docker-compose exec api_backend pylint --rcfile ./api_backend/pylintrc ./api_backend
```

Next, we perform additional checks to verify, and possibly correct, the code formatting 
(using `black`) and the ordering and organization of import statements (using `isort`).

```bash
$ docker-compose exec api_backend black . --check
$ docker-compose exec api_backend isort . --check-only
```
