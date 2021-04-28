DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Accounts;
DROP TABLE IF EXISTS Offers;

CREATE TABLE Events(
    event_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    event_time INTEGER,
    event_title VARCHAR(255) NOT NULL
);

CREATE TABLE Users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_fname VARCHAR(50) NOT NULL,
    user_sname VARCHAR(50) NOT NULL,
    user_dob DATETIME NOT NULL,
    user_address VARCHAR(255),
    user_country VARCHAR(100),
    user_state VARCHAR(100),
    user_postcode INTEGER,
    user_phone INTEGER,
    user_email VARCHAR(255) NOT NULL
);

CREATE TABLE Accounts(
    account_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    account_balance INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE Offers(
    offer_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    offer_odds INTEGER NOT NULL,
    offer_amount INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    FOREIGN KEY (buyer_id) REFERENCES Users (user_id)
);