# RESTful API for Personal Reading List

The project provides python flask RESTful API for building a personal reading list. It uses external RESTful service to complement its functionality.

The external API comes from OpenLibrary.

https://openlibrary.org/dev/docs/api/books


## 1. Basic Task

### 1.1 External API

```
@app.route("/detail/<type>/<index>")
```
This api interacts with external Openlibrary api. It provided the detail of a book on Openlibrary based on the identity number of a book.

Parameter \<type\> is for type of identity number.According to document, it currently support 4 type, including ISBN, OCLC, LCCN, OLID. Parameter \<index\> is the identity number.

### 1.2 External Cloud Database

In this project, we choose MongoDB for persisting information. MongoDB is a popular NoSQL database, the basic unit of MongoDB is document. It is flexibale and ideal for keeping json. 

#### 1.2.1 MongoDB Set Up

#### 1.2.2 Implement Interface In Python

### 1.3 CURD Operations

```
@app.route("/mylibrary")
```

#### 1.3.1 GET 

#### 1.3.2 POST

#### 1.3.3 PUT

#### 1.3.4 DELETE

## 2. Adavanced Task