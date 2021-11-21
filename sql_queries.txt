CREATE TABLE ToVerify (
	first_name varchar(60),
    last_name varchar(60),
    user_name varchar(60),
    user_pass varchar(60),
    email varchar(60),
    verification_code varchar(20)
);

CREATE TABLE Users (
    id int PRIMARY KEY Not NUll,
	first_name varchar(60),
    last_name varchar(60),
    user_name varchar(60),
    user_pass varchar(60)
);

CREATE TABLE ClientAccount (
    id int NOT NULL PRIMARY KEY,
	client int,
	user int,
	FOREIGN KEY (client) REFERENCES Client(id),
    FOREIGN KEY (user) REFERENCES Users(id)
);

CREATE TABLE Vendor (
    id int NOT NULL PRIMARY KEY,
	company int NOT NULL,
	name varchar(30) NOT NULL,
	uuid varchar(40) NOT NULL,
    FOREIGN KEY (company) REFERENCES Company(id)
);

CREATE TABLE Company (
    id int NOT NULL PRIMARY KEY,
	name varchar(30) NOT NULL,
	default_currency int NOT NULL,
    FOREIGN KEY (default_currency) REFERENCES Currency(id)
);

CREATE TABLE Employee (
    id int NOT NULL PRIMARY KEY,
	company int NOT NULL,
	user int NOT NULL,
    FOREIGN KEY (company) REFERENCES Company(id),
	FOREIGN KEY (user) REFERENCES Users(id)
);

CREATE TABLE CompanyDetails (
    id int NOT NULL PRIMARY KEY,
	company int NOT NULL,
	address varchar(30),
    zip varchar(30),
    city varchar(30),
    country varchar(30),
    email varchar(30),
    phone varchar(30),
    vat_id varchar(30),
    commerce_id varchar(30),
    FOREIGN KEY (company) REFERENCES Company(id)
);

CREATE TABLE VendorDetails (
    id int NOT NULL PRIMARY KEY,
	vendor int NOT NULL,
	address varchar(30),
    zip varchar(30),
    city varchar(30),
    country varchar(30),
    email varchar(30),
    phone varchar(30),
    vat varchar(30),
    commerce varchar(30),
    FOREIGN KEY (vendor) REFERENCES Vendor(id)
);

CREATE TABLE ClientDetails (
    id int NOT NULL PRIMARY KEY,
	client int NOT NULL,
	address varchar(30),
    zip varchar(30),
    city varchar(30),
    country varchar(30),
    email varchar(30),
    phone varchar(30),
    vat varchar(30),
    commerce varchar(30),
    FOREIGN KEY (client) REFERENCES Client(id)
);

CREATE TABLE Currency (
    id int NOT NULL PRIMARY KEY,
    name varchar(20),
    code varchar(5)
);

CREATE TABLE Bill (
    id int NOT NULL PRIMARY KEY,
	vendor int NOT NULL,
	currency int NOT NULL,
    referance int,
    uuid varchar(40) NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vendor) REFERENCES Vendor(id),
	FOREIGN KEY (currency) REFERENCES Currency(id),
    FOREIGN KEY (referance) REFERENCES Users(id)
);


CREATE TABLE BankAccount (
    id int NOT NULL PRIMARY KEY,
	company int NOT NULL,
	start_amount FLOAT NOT NULL,
	name varchar(40) NOT NULL,
    iban varchar(40) NOT NULL,
	currency int NOT NULL,
    uuid varchar(40) NOT NULL,
    FOREIGN KEY (company) REFERENCES Company(id),
	FOREIGN KEY (currency) REFERENCES Currency(id)
);

CREATE TABLE Client (
    id int NOT NULL PRIMARY KEY,
	company int NOT NULL,
	name varchar(40) NOT NULL,
    uuid varchar(40) NOT NULL,
    FOREIGN KEY (company) REFERENCES Company(id)
);

CREATE TABLE Invoice (
    id int NOT NULL PRIMARY KEY,
	client int NOT NULL,
    currency int NOT NULL,
    referance int,
    uuid varchar(40) NOT NULL,
    FOREIGN KEY (client) REFERENCES Client(id),
    FOREIGN KEY (company) REFERENCES Company(id),
    FOREIGN KEY (referance) REFERENCES Users(id)
);

CREATE TABLE InvoiceSent (
    id int NOT NULL PRIMARY KEY,
    invoice int NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (invoice) REFERENCES Invoice(id)
);

CREATE TABLE InvoicePaid (
    id int NOT NULL PRIMARY KEY,
    invoice int NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (invoice) REFERENCES Invoice(id)
);

CREATE TABLE InvoiceViewed (
    id int NOT NULL PRIMARY KEY,
    invoice int NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (invoice) REFERENCES Invoice(id)
);

CREATE TABLE Item (
    id int NOT NULL PRIMARY KEY,
    company int NOT NULL,
	description varchar(240),
    default_price FLOAT DEFAULT 0,
    uuid varchar(40) NOT NULL,
    FOREIGN KEY (company) REFERENCES Company(id)
);

CREATE TABLE BillItem (
    id int NOT NULL PRIMARY KEY,
    bill int NOT NULL,
	item INT NOT NULL,
    price FLOAT DEFAULT 0,
    amount int DEFAULT 0,
    FOREIGN KEY (bill) REFERENCES Bill(id),
	FOREIGN KEY (item) REFERENCES Item(id)
);

CREATE TABLE InvoiceItem (
    id int NOT NULL PRIMARY KEY,
    invoice int NOT NULL,
	item INT NOT NULL,
    price FLOAT DEFAULT 0,
    amount int DEFAULT 0,
    FOREIGN KEY (invoice) REFERENCES Invoice(id),
	FOREIGN KEY (item) REFERENCES Item(id)
);