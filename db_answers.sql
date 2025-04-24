
USE library;

CREATE TABLE IF NOT EXISTS user_role
(
    roleid integer NOT NULL PRIMARY KEY,
    role_name varchar(80) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users
(
    userid integer NOT NULL PRIMARY KEY,
    fname varchar(80) NOT NULL,
    lname varchar(80) NOT NULL,
    username varchar(80) NOT NULL UNIQUE,
    tel varchar(10) NOT NULL UNIQUE,
    joined date NOT NULL,
    role integer,
    FOREIGN KEY (role) REFERENCES user_role(roleid)
);

CREATE TABLE IF NOT EXISTS staff
(
    staffid integer NOT NULL PRIMARY KEY,
    fname varchar(80)  NOT NULL,
    lname varchar(80)  NOT NULL,
    username varchar(80) NOT NULL UNIQUE,
    tel varchar(10) NOT NULL UNIQUE,
    joined date NOT NULL,
    staff_role integer,
    FOREIGN KEY (staff_role) REFERENCES user_role(roleid)
);

CREATE TABLE IF NOT EXISTS bookgenre
(
    genreid integer NOT NULL PRIMARY KEY,
    genre_name varchar(80) NOT NULL UNIQUE
    
);


CREATE TABLE IF NOT EXISTS books
(
    bookid integer NOT NULL PRIMARY KEY,
    title varchar(80)  NOT NULL,
    isbn varchar(80) NOT NULL UNIQUE,
    author varchar(80) NOT NULL,
    publisher varchar(80) NOT NULL,
    year date NOT NULL,
    total_copies integer NOT NULL,
    available_copies integer NOT NULL,
    book_genre integer,
    FOREIGN KEY (book_genre) REFERENCES bookgenre(genreid)
);

CREATE TABLE IF NOT EXISTS  bookloans
(
    loanid integer NOT NULL PRIMARY KEY,
    bookid integer NOT NULL,
    FOREIGN KEY (bookid) REFERENCES books(bookid),
    borrow_date date NOT NULL,
    due_date date NOT NULL,
    return_date date,
    status varchar(80)  NOT NULL,
    borrower_id integer,
    FOREIGN KEY (borrower_id) REFERENCES users(userid)
);

CREATE TABLE IF NOT EXISTS fines
(
    fineid integer NOT NULL PRIMARY KEY,
    loan_id integer NOT NULL,
    finee_id integer NOT NULL,
    FOREIGN KEY (finee_id) REFERENCES users(userid)
    FOREIGN KEY (loan_id) REFERENCES bookloans(loanid),
    amount integer NOT NULL,
    reason varchar(100)  NOT NULL,
    paid boolean NOT NULL
);


-- Sample Data
INSERT INTO user_role (roleid, role_name) VALUES
(1, 'Admin'),
(2, 'Librarian'),
(3, 'Member');


INSERT INTO users (userid, fname, lname, username, tel, joined, role) VALUES
(1, 'John', 'Doe', 'johndoe', '1234567890', '2023-01-01', 1),
(2, 'Jane', 'Smith', 'janesmith', '9876543210', '2023-02-15', 3),
(3, 'Alice', 'Johnson', 'alicejohnson', '5555555555', '2023-03-20', 2);

INSERT INTO staff (staffid, fname, lname, username, tel, joined, staff_role) VALUES
(1, 'Sara', 'Williams', 'sarawilliams', '1231231234', '2023-01-01', 1),
(2, 'Mark', 'Taylor', 'marktaylor', '3213214321', '2023-02-15', 2);

INSERT INTO bookgenre (genreid, genre_name) VALUES
(1, 'Fiction'),
(2, 'Non-Fiction'),
(3, 'Science Fiction'),
(4, 'Biography');

INSERT INTO books (bookid, title, isbn, author, publisher, year, total_copies, available_copies, book_genre) VALUES
(1, 'To Kill a Mockingbird', '9780061120084', 'Harper Lee', 'J.B. Lippincott & Co.', '1960-07-11', 10, 8, 1),
(2, '1984', '9780451524935', 'George Orwell', 'Secker & Warburg', '1949-06-08', 5, 3, 2),
(3, 'Dune', '9780441013593', 'Frank Herbert', 'Chilton Books', '1965-08-01', 7, 5, 3),
(4, 'The Diary of a Young Girl', '9780553296983', 'Anne Frank', 'Contact Publishing', '1947-06-25', 6, 6, 4);

INSERT INTO bookloans (loanid, bookid, borrow_date, due_date, return_date, status, borrower_id) VALUES
(1, 1, '2023-04-01', '2023-04-15', NULL, 'Borrowed', 2),
(2, 2, '2023-04-10', '2023-04-24', '2023-04-22', 'Returned', 3),
(3, 3, '2023-04-05', '2023-04-19', NULL, 'Borrowed', 1);

INSERT INTO fines (fineid, loan_id, amount, reason, paid, finee_id) VALUES
(1, 1, 5, 'Late return', FALSE, 1),
(2, 3, 10, 'Late return', TRUE, 2);
