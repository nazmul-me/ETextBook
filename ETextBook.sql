SET GLOBAL sql_mode = '';

CREATE TABLE ETextBook.User (
    userID INT PRIMARY KEY,
    firstName VARCHAR(20),
    lastName VARCHAR(20),
    email VARCHAR(50),
    password VARCHAR(20),
    role TEXT CHECK (role IN ('Admin', 'TA', 'Faculty', 'Student')),
    account_creation_date DATE DEFAULT '0000-00-00 00:00:00'
);


CREATE TABLE ETextBook.Admin(
    AID INT PRIMARY KEY,
    FOREIGN KEY (AID) REFERENCES User(userID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE ETextBook.TA(
    TAID INT PRIMARY KEY,
    FOREIGN KEY (TAID) REFERENCES User(userID) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE ETextBook.Faculty(
    FID INT PRIMARY KEY,
    FOREIGN KEY (FID) REFERENCES User(userID) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE ETextBook.Student(
    SID INT PRIMARY KEY,
    FOREIGN KEY (SID) REFERENCES User(userID) ON DELETE CASCADE ON UPDATE CASCADE
);
