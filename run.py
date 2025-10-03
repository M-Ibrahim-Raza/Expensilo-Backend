"""
Example usage of the models
"""

from db.db_setup import get_db, init_db
from models import User, Category, UserCategory, Transaction, UserTransaction
from datetime import datetime


def create_sample_data():
    """Create sample data to demonstrate the models"""

    # Initialize database (create tables)
    init_db()

    with get_db() as db:
        # Create a user
        user = User(
            name="John Doe",
            email="john@example.com",
            password="hashed_password_here",
            preferences='{"theme": "dark", "currency": "USD"}',
        )
        db.add(user)
        db.flush()  # Get user.id without committing

        # Create categories
        food_category = Category(name="Food")
        transport_category = Category(name="Transport")
        salary_category = Category(name="Salary")

        db.add_all([food_category, transport_category, salary_category])
        db.flush()

        # Associate categories with user
        user_cat1 = UserCategory(user_id=user.id, category_id=food_category.id)
        user_cat2 = UserCategory(user_id=user.id, category_id=transport_category.id)
        user_cat3 = UserCategory(user_id=user.id, category_id=salary_category.id)

        db.add_all([user_cat1, user_cat2, user_cat3])
        db.flush()

        # Create transactions
        # Expense transaction (negative amount)
        expense_transaction = Transaction(
            category_id=food_category.id, title="Grocery Shopping"
        )

        # Income transaction (positive amount)
        income_transaction = Transaction(
            category_id=salary_category.id, title="Monthly Salary"
        )

        db.add_all([expense_transaction, income_transaction])
        db.flush()

        # Link transactions to user with amounts
        user_expense = UserTransaction(
            user_id=user.id,
            transaction_id=expense_transaction.id,
            amount=-150.50,  # Negative for expense
            details="Bought groceries at Walmart",
            date=datetime.now(),
        )

        user_income = UserTransaction(
            user_id=user.id,
            transaction_id=income_transaction.id,
            amount=5000.00,  # Positive for income
            details="Monthly salary payment",
            date=datetime.now(),
        )

        db.add_all([user_expense, user_income])

        print("Sample data created successfully!")


def query_examples():
    """Examples of querying the data"""

    with get_db() as db:
        # Get all users with their categories
        users = db.query(User).all()
        for user in users:
            print(f"\nUser: {user.name}")
            print(f"Categories: {[uc.category.name for uc in user.categories]}")

            # Calculate total balance
            total = sum(ut.amount for ut in user.transactions)
            print(f"Balance: ${total:.2f}")

            # Show transactions
            for ut in user.transactions:
                trans_type = "Income" if ut.amount > 0 else "Expense"
                print(f"  {trans_type}: {ut.transaction.title} - ${abs(ut.amount):.2f}")


if __name__ == "__main__":
    # Uncomment to run examples
    # create_sample_data()
    # query_examples()
    pass
