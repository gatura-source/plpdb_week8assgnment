
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..db import get_db
from ..auth.auth_jwt import get_current_user
from pydantic import BaseModel
from datetime import datetime

user_route = APIRouter()

@user_route.get('/member/myloans')
def hello(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    username = current_user["sub"]
    loanee = db.execute(text("SELECT * FROM users WHERE username = :username"), {"username": username})
    loanee_id = loanee.fetchone()._asdict()['userid']
    result = db.execute(text("SELECT * FROM bookloans WHERE borrower_id = :uid"), {"uid": loanee_id})
    loans = result.mappings()
    return {"Loans": f"Loans: {[(row) for row in loans]}"}

@user_route.get('/member/available_books')
def available(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    available_books = db.execute(text("SELECT * FROM books WHERE available = 1 "))
    books = available_books.mappings()
    return {"books": f"{[book for book in books]}"}

class Loan(BaseModel):
    book_id: int
@user_route.post('/member/loan')
def loan(loan: Loan, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # check that current user has no loans or fines first
    username = current_user["sub"]
    
    # Check if the user has any ongoing loans
    user_id = db.execute(text("SELECT userid FROM users WHERE username = :username"), {'username': username}).fetchone()._asdict()
    if user_id is None:
        return {"message": "User not found"}
    
    user_id = user_id['userid']
    
    # Fetch the number of loans and fines the user has
    loans = db.execute(text("SELECT COUNT(*) FROM bookloans WHERE borrower_id = :uid AND status = 'Borrowed'"), {"uid": user_id}).scalar()
    fines = db.execute(text("SELECT COUNT(*) FROM fines WHERE finee_id = :uid AND paid = FALSE"), {"uid": user_id}).scalar()

    if loans > 0 or fines > 0:
        return {"message": "Cannot loan with an existing loan or unpaid fine"}

    # Check if the book is available
    book = db.execute(text("SELECT * FROM books WHERE bookid = :book_id"), {"book_id": loan.book_id}).fetchone()._asdict()

    if book is None:
        return {"message": "Book not found"}
    
    if book['available_copies'] > 0:
        # Proceed with loaning the book
        db.execute(text("""
            INSERT INTO bookloans (bookid, borrower_id, borrow_date, due_date, status)
            VALUES (:book_id, :user_id, NOW(), DATE_ADD(NOW(), INTERVAL 14 DAY), 'Borrowed')
        """), {'book_id': loan.book_id, 'user_id': user_id})
        
        # Update available copies in the books table
        db.execute(text("UPDATE books SET available_copies = available_copies - 1 WHERE bookid = :book_id"), {"book_id": loan.book_id})
        
        db.commit()  # Commit the transaction
        return {"message": "Book loaned successfully"}
    else:
        return {"message": "Book not available for loan"}


@user_route.post('/member/return')
def loan_return(loan: Loan, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
     # check that current user has no loans or fines first
    username = current_user["sub"]
    
    # Check if the user has any ongoing loans
    user_id = db.execute(text("SELECT userid FROM users WHERE username = :username"), {'username': username}).fetchone()._asdict()
    if user_id is None:
        return {"message": "User not found"}
    
    user_id = user_id['userid']
    
    # Fetch the loan
    loan_f = db.execute(text("SELECT * FROM bookloans WHERE bookid = :book_id"), {"book_id": loan.book_id}).fetchone()._asdict()
    if loan_f is None:
        return ({"message": "Loan not Found"})
    db.execute(text("UPDATE  bookloans SET status = 'Returned' WHERE bookid = :book_id"), {"book_id": loan.book_id})
    db.execute(text("UPDATE  bookloans SET return_date = NOW() WHERE bookid = :book_id"), {"book_id": loan.book_id})
    db.execute(text("UPDATE books SET available_copies = available_copies + 1 WHERE bookid = :book_id"), {"book_id": loan.book_id})
     # Fine if returned late
    due_date = loan_f["due_date"]
    return_date = datetime.now()

    if return_date.date() > due_date:
        
        fine_amount = 100

        db.execute(text("""
            INSERT INTO fines (finee_id, loan_id, amount, reason, paid)
            VALUES (:finee_id, :loan_id, :amount, :reason, FALSE)
        """), {
            "finee_id": user_id,
            "loan_id": loan_f['loanid'],
            "amount": fine_amount,
            "reason": "Late book return"
        })
    db.commit()
    return ({"message": "Loan return success"})

@user_route.get('/member/myfines')
def myfines(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    user = current_user["sub"]
    user_id = db.execute(text("SELECT userid FROM users WHERE username = :usrname"), {"usrname": user}).fetchone()._asdict()['userid']
    if user_id is not None:
        fines = db.execute(text("SELECT * FROM fines WHERE finee_id = :id"), {'id': user_id}).mappings()
        return ({"fines": [fine for fine in fines]})
    

class FinePayment(BaseModel):
    amount: int
    fineid: int
@user_route.post('/member/payfine')
def payfine(fine: FinePayment, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    #get fine
    fine_f = db.execute(text("SELECT * FROM fines WHERE fineid = :f_id"), {"f_id": fine.fineid}).fetchone()._asdict()
    if fine_f is not None:
        if fine_f['amount'] == fine.amount:
            db.execute(text("UPDATE fines SET paid = 1 WHERE fineid = :f_id"), {"f_id": fine.fineid})
            db.commit()
            return ({"message": "Fine full payment success"})
        else:
            db.execute(text("UPDATE fines SET amount = amount - :amnt WHERE fineid = :f_id"), {"f_id": fine.fineid, "amnt": fine.amount})
            db.commit()
            return ({"message": f"Fine partial payment of amount : {fine.amount} success!"})
    