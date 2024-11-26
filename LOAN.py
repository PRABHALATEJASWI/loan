from datetime import datetime, timedelta

# Simulating a simple in-memory "database" with dictionaries
loans = {}
repayments = {}

def generate_repayments(loan_id, amount, term, start_date):
    """Generate the repayment schedule for the loan."""
    weekly_payment = amount / term
    repayments_for_loan = []
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    for i in range(term):
        due_date = start_date + timedelta(weeks=i+1)
        repayments_for_loan.append({
            'loan_id': loan_id,
            'due_date': due_date.strftime('%Y-%m-%d'),
            'amount_due': round(weekly_payment, 2),
            'status': 'PENDING'
        })
    
    return repayments_for_loan

def create_loan():
    """Create a new loan request."""
    user_id = int(input("Enter user ID: "))
    amount = float(input("Enter loan amount: $"))
    term = int(input("Enter loan term (in weeks): "))
    start_date = input("Enter loan start date (YYYY-MM-DD): ")
    
    # Generate repayments for the loan
    loan_repayments = generate_repayments(len(loans) + 1, amount, term, start_date)
    
    loan_id = len(loans) + 1
    loans[loan_id] = {
        'loan_id': loan_id,
        'user_id': user_id,
        'amount': amount,
        'term': term,
        'start_date': start_date,
        'status': 'PENDING',
        'repayments': loan_repayments
    }
    
    print(f"Loan created successfully with Loan ID {loan_id}.")
    return loan_id

def approve_loan():
    """Approve a loan by changing its status to 'APPROVED'."""
    loan_id = int(input("Enter the loan ID to approve: "))
    if loan_id not in loans:
        print("Loan not found.")
        return

    loans[loan_id]['status'] = 'APPROVED'
    print(f"Loan {loan_id} has been approved.")

def view_loan():
    """View loan details."""
    user_id = int(input("Enter your user ID to view your loan: "))
    loan_id = int(input("Enter loan ID: "))
    
    if loan_id not in loans:
        print("Loan not found.")
        return
    
    loan = loans[loan_id]
    
    if loan['user_id'] != user_id:
        print("Unauthorized: You cannot view this loan.")
        return
    
    print(f"Loan ID: {loan_id}")
    print(f"Amount: ${loan['amount']}")
    print(f"Term: {loan['term']} weeks")
    print(f"Start Date: {loan['start_date']}")
    print(f"Status: {loan['status']}")
    print("Repayments:")
    for repayment in loan['repayments']:
        print(f"  Due Date: {repayment['due_date']}, Amount Due: ${repayment['amount_due']}, Status: {repayment['status']}")

def make_repayment():
    """Make a repayment for a loan."""
    user_id = int(input("Enter your user ID: "))
    loan_id = int(input("Enter loan ID for repayment: "))
    amount = float(input("Enter repayment amount: $"))
    
    if loan_id not in loans:
        print("Loan not found.")
        return
    
    loan = loans[loan_id]
    
    if loan['user_id'] != user_id:
        print("Unauthorized: You cannot make a repayment for this loan.")
        return
    
    # Check and update repayments
    for repayment in loan['repayments']:
        if repayment['status'] == 'PENDING' and amount >= repayment['amount_due']:
            repayment['status'] = 'PAID'
            repayments[loan_id] = repayments.get(loan_id, [])
            repayments[loan_id].append(repayment)
            print(f"Repayment of ${amount} made successfully for Loan ID {loan_id}.")
            break
    else:
        print("No pending repayments or insufficient repayment amount.")

    # Check if the loan is fully paid
    if all(r['status'] == 'PAID' for r in loan['repayments']):
        loan['status'] = 'PAID'
        print(f"Loan ID {loan_id} is now fully paid.")

def menu():
    """Main menu to interact with the loan system."""
    while True:
        print("\nLoan Application System")
        print("1. Create Loan")
        print("2. Approve Loan (Admin)")
        print("3. View Loan Details")
        print("4. Make Repayment")
        print("5. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            create_loan()
        elif choice == '2':
            approve_loan()
        elif choice == '3':
            view_loan()
        elif choice == '4':
            make_repayment()
        elif choice == '5':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice, please try again.")

# Run the menu system
menu()
