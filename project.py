import calendar
import datetime

class Expense:
    def __init__(self, expense_name: str, expense_type: str, cost: float) -> None:
        self.expense_name = expense_name
        self.expense_type = expense_type
        self.cost = cost

    def display(self) -> str:
        return f"Expense Entry: {self.expense_name} | Category: {self.expense_type} | Cost: ${self.cost:,.2f}"


def run_tracker():
    print("🚀 Launching Budget Manager!")
    record_file = "expense_records.csv"
    total_budget = 2000  # Set your total budget

    user_expense = capture_expense()
    store_expense(user_expense, record_file)
    analyze_expenses(record_file, total_budget)


def capture_expense():
    print("🔹 Enter Your Expense Details")
    item_name = input("Expense Name: ")
    
    while True:
        try:
            item_cost = float(input("Expense Amount: "))
            if item_cost < 0:
                print("⚠️ Expense amount must be positive. Try again.")
            else:
                break
        except ValueError:
            print("⚠️ Invalid amount! Please enter a valid number.")

    expense_types = ["Meals", "Housing", "Office", "Leisure", "Miscellaneous"]

    while True:
        print("Choose a category: ")
        for i, category in enumerate(expense_types, start=1):
            print(f"  {i}. {category}")

        try:
            selected_index = int(input(f"Enter a number [1 - {len(expense_types)}]: ")) - 1
            if 0 <= selected_index < len(expense_types):
                chosen_category = expense_types[selected_index]
                return Expense(item_name, chosen_category, item_cost)
            else:
                print("⚠️ Invalid selection! Try again.")
        except ValueError:
            print("⚠️ Please enter a valid number.")


def store_expense(expense: Expense, record_file):
    print(f"📌 Saving Expense: {expense.display()} into {record_file}")
    with open(record_file, "a", encoding="utf-8") as file:  # ✅ Fixed Unicode Issue
        file.write(f"{expense.expense_name},{expense.cost},{expense.expense_type}\n")


def analyze_expenses(record_file, total_budget):
    print("\n📊 Generating Expense Summary...\n")
    recorded_expenses = []

    try:
        with open(record_file, "r", encoding="utf-8") as file:  # ✅ Read file using UTF-8
            lines = file.readlines()
            for line in lines:
                name, cost, category = line.strip().split(",")
                recorded_expenses.append(Expense(name, category, float(cost)))

        category_totals = {}
        for expense in recorded_expenses:
            category_totals[expense.expense_type] = category_totals.get(expense.expense_type, 0) + expense.cost

        print("📌 Expenses by Category:")
        for category, amount in category_totals.items():
            print(f"  {category}: ${amount:.2f}")

        total_spent = sum(item.cost for item in recorded_expenses)
        remaining_budget = total_budget - total_spent

        print(f"\n💰 Total Spent: ${total_spent:.2f}")
        print(f"✅ Remaining Budget: ${remaining_budget:.2f}")

        today = datetime.datetime.now()
        days_this_month = calendar.monthrange(today.year, today.month)[1]
        days_left = days_this_month - today.day

        daily_allowance = remaining_budget / days_left if days_left > 0 else 0
        print(highlight_text(f"➡️ Suggested Daily Spending: ${daily_allowance:.2f}"))

    except FileNotFoundError:
        print("⚠️ No expense records found. Add an expense first.")


def highlight_text(content):
    return f"\033[94m{content}\033[0m"


if __name__ == "__main__":
    run_tracker()
