from expense import Expense
import datetime
import calendar

def main():
    # Starting the Expense Tracker program
    print(colored_text(f"Running Expense Tracker!", "blue"))
    expense_file_path = "expenses.csv"  # File path for storing expenses
    budget = 2000  # Monthly budget amount

    # Get user input on a new expense
    expense = get_user_expense()

    # Save the user expense to the file
    save_expense_to_file(expense, expense_file_path)

    # Summarize all expenses from the file and compare with the budget
    summarize_expenses(expense_file_path, budget)

def get_user_expense():
    """Prompt the user for expense details: name, amount, and category."""
    print(f"Getting User Expense")

    # Get expense name and amount from user
    expense_name = input("Enter expense name: ")
    
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            if expense_amount < 0:
                raise ValueError("Amount cannot be negative.")
            break
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a valid number.")

    # List of predefined expense categories
    expense_categories = [
        "Housing 🏠", 
        "Transportation 🚗", 
        "Food 🍽️", 
        "Entertainment 🎮", 
        "Health 🏥",
        "Education 📚",
        "Savings/Investments 💰",
        "Shopping 🛍️",
        "Debt Payments 💳",
        "Personal Care 💅",
        "Miscellaneous 🎁",
        "Travel ✈️",
    ]

    # Prompt the user to select a category
    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f" {i+1}. {colored_text(category_name, 'orange')}")  # Orange text for categories

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        # Ensure the selected category is valid
        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            # Return the expense details as an Expense object
            return Expense(
                name=expense_name, category=selected_category, amount=expense_amount
            )
        else:
            print("Invalid Category. Try again!")

def save_expense_to_file(expense: Expense, expense_file_path):
    """Save the expense details to a CSV file."""
    print(f"Saving User Expense: {expense} to {expense_file_path}")
    try:
        # Open the file with utf-8 encoding to handle special characters like emojis
        with open(expense_file_path, "a", encoding="utf-8") as f:
            f.write(f"{expense.name},{expense.amount},{expense.category}\n")
    except Exception as e:
        print(f"An error occurred while saving the expense: {e}")

def summarize_expenses(expense_file_path, budget):
    """Summarize the expenses from the CSV file and compare them with the budget."""
    print(colored_text(f" Summarizing User Expense", "blue"))
    expenses: list[Expense] = []

    try:
        with open(expense_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()  # Read all lines from the file
            
            if not lines:
                print("No expenses recorded yet.")
                return
            
            for line in lines:
                # Ensure the line has exactly three parts
                parts = line.strip().split(",")
                if len(parts) != 3:
                    print(f"Skipping invalid line: {line.strip()}")
                    continue
                
                expense_name, expense_amount, expense_category = parts
                expenses.append(
                    Expense(
                        name=expense_name,
                        amount=float(expense_amount),
                        category=expense_category,
                    )
                )

    except FileNotFoundError:
        print(f"File not found: {expense_file_path}. Please make sure the file exists.")
        return
    except Exception as e:
        print(f"An error occurred while reading expenses: {e}")
        return

    # Calculate total spending by category
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    # Display the expenses by category
    print("💸 Expenses by Category")
    for key, amount in amount_by_category.items():
        print(f"  {colored_text(key, 'orange')}: ${amount:.2f}")

    # Calculate and display the total amount spent
    total_spent = sum(expense.amount for expense in expenses)
    print(colored_text(f"💵 Total Spent: ${total_spent:.2f} this month!", "red"))

    # Calculate and display the remaining budget
    remaining_budget = budget - total_spent
    print(colored_text(f"📊 Budget Remaining: ${remaining_budget:.2f}!", "green"))

    # Calculate the number of days left in the current month
    today = datetime.date.today()
    total_days_in_month = calendar.monthrange(today.year, today.month)[1]
    remaining_days = total_days_in_month - today.day

    # Calculate and display the daily budget for the remaining days
    daily_budget = remaining_budget / remaining_days if remaining_days > 0 else 0
    print(colored_text(f"📅 Daily Budget Remaining: ${daily_budget:.2f}", "green"))



def colored_text(text, color):
    """Return colored text for terminal output based on the color provided."""
    color_codes = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "orange": "\033[93m",  # Using yellow for orange
        "reset": "\033[0m"
    }
    return f"{color_codes[color]}{text}{color_codes['reset']}"

if __name__ == "__main__":
    main()
