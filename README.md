# Habi Api

This is a simple API with Serverless framework.

**For requirement number 1 there's no state field on property table so this field was omitted on filters**

## Example request

```shell
# All filters are optional
curl --location --request GET 'http://localhost:3000/properties?status=5,3&city=medellin&year=2000'
```

## Contents

This template includes the following extra configurations:

- [serverless framework][1]
- [serverless-offline plugin][2]
- [serverless-prune-plugin][8]
- [serverless-python-requirements][9]
- [yapf][3] code formatter
- [Pylint][4] for code linting
- [Poetry][5] For virtual environment

It will, by default set the stage to `dev` and the region to `us-east-1`.

## Installation

1. Create new virtual environment

  ```shell
  make venv
  ```

2. Install Python dependencies

  ```shell
  make install
  ```
  
3. Install Serverless and Node dependencies

  ```shell
  make npmi
  ```
  
4. Execute local server

  ```shell
  make run
  ```


## Formatting, linting and complexity check

```shell
make fmt
```

```shell
make lint
```

```shell
make complexity
```

## Explanation of the project.

### General explanation

This simple API has been implemented with the hexagonal architecture for the general project structure, 
repository pattern for the data access manipulation and the python decorator patter for all the project
middlewares.

Hexagonal architecture brings the better abstraction over the business logic and all the data manipulation,
giving the ability to replace components or extend it easily.

Repository pattern creates the lightest abstraction over the data access comparing with a traditional ORM 
implementation. This brings the ability of create complex queries with better performance. A cons of this
patter are the runtime errors by malformed SQL queries sins there is no check until query is running.

Decorator pattern is a great choice to generate Middlewares and isolate request logic and transformation
from all the business and data access logic, also makes easy to maintain all code in general.

### Requirement number 2 explanation

![DB-ER-diagram](https://raw.githubusercontent.com/danteay/hapi-api/master/Habi-Liked.png)

If we continue to use same DB structure, in order to keep tracking of all property likes of the any user
we should implement the DB structure of the past image and create the `liked` and `liked_history` tables,
where the `table` will keep the current liked properties of a user and can be deleted it at any time. To keep
history track for all liked properties the `liked_history` table will keep any type of liked movement (liked
or unliked) and keep the relation between property, user and the time of the movement execution

If we could choose any other DB to store Liked properties I would suggest AWS QLDB (AWS Quantum Ledger Data Base).
This database keep tracking of all the historic changes of a record even when the record was deleted. This DB has
immutable records so, any modification of a record at the end is a new record with new values and the DB keeps
the latest value for that entry.

[1]: https://serverless.com/
[2]: https://github.com/dherault/serverless-offline
[3]: https://github.com/google/yapf
[4]: http://pylint.pycqa.org/en/latest/
[5]: https://python-poetry.org/
[8]: https://github.com/claygregory/serverless-prune-plugin
[9]: https://github.com/UnitedIncome/serverless-python-requirements
