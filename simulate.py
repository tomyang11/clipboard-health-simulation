import matplotlib.pyplot as plt

def calculate_monthly_revenue(customers, customer_tenure, account_managers, base_revenue):
    managed_customers = min(account_managers * 25, customers)
    unmanaged_customers = customers - managed_customers

    account_manager_revenue = 0
    additional_revenue = 0
    for i in range(managed_customers):
        month = customer_tenure[i]
        customer_revenue = base_revenue * ((1 + 0.2) ** min(month, 6) - 1)
        additional_revenue += customer_revenue
        account_manager_revenue += customer_revenue + base_revenue
    
    monthly_revenue = managed_customers * base_revenue + additional_revenue + unmanaged_customers * base_revenue
    return monthly_revenue, account_manager_revenue

def calculate_new_business_revenue(new_business_personnel, new_customer_rate, base_revenue):
    new_customers = new_business_personnel * new_customer_rate
    return new_customers * base_revenue

# def calculate_support_revenue(support_personnel, base_churn_rate, customers, base_revenue):
#     # Assuming support reduces churn rate
#     reduced_churn = customers * base_churn_rate * (0.85 ** support_personnel)
#     retained_customers = (customers * base_churn_rate) - reduced_churn
#     return retained_customers * base_revenue

def calculate_churn_rate(base_churn_rate, csat_increase):
    new_churn_rate = base_churn_rate * (0.85 ** csat_increase)
    return max(new_churn_rate, 0)

def update_customer_tenure(customer_tenure, account_managers, total_customers):
    managed_customers = min(account_managers * 25, total_customers)
    for i in range(total_customers):
        if i < managed_customers:
            customer_tenure[i] = min(customer_tenure[i] + 1, 6)
        else:
            customer_tenure[i] = 0
    return customer_tenure

def run_simulation():
    total_months = 24
    total_personnel = 20
    customers = 1000
    base_revenue = 100
    base_churn_rate = 0.10
    customer_tenure = [0] * customers
    cumulative_revenue = 0

    monthly_revenues = []
    account_manager_revenues = []
    cumulative_revenues = []
    new_business_revenues = []
    support_revenues = []

    for month in range(1, total_months + 1):
        print(f"Month {month}: Please allocate the 20 personnel among the three roles.")
        new_business = int(input("Enter number of personnel for New Business Acquisition: "))
        account_management = int(input("Enter number of personnel for Account Management: "))
        support = int(input("Enter number of personnel for Support: "))
        while new_business + account_management + support != total_personnel:
            print("The total personnel allocation does not match 20. Please re-enter the values.")
            new_business = int(input("Enter number of personnel for New Business Acquisition: "))
            account_management = int(input("Enter number of personnel for Account Management: "))
            support = int(input("Enter number of personnel for Support: "))
        customer_tenure = update_customer_tenure(customer_tenure, account_management, customers)

        new_customers = (new_business * 5) + 25
        csat_increase = support
        churn_rate = calculate_churn_rate(base_churn_rate, csat_increase)

        lost_customers = int(customers * churn_rate)
        customers += (new_customers - lost_customers)

        if len(customer_tenure) < customers:
            # Extend the customer_tenure list to match the new customer count
            customer_tenure.extend([0] * (customers - len(customer_tenure)))
        elif len(customer_tenure) > customers:
            # Reduce the customer_tenure list to match the new customer count
            customer_tenure = customer_tenure[:customers]

        monthly_revenue, manager_revenue = calculate_monthly_revenue(customers, customer_tenure, account_management, base_revenue)
        
        new_business_revenue = calculate_new_business_revenue(new_business, 5, base_revenue)  # Calculate revenue from new business
        # support_revenue = calculate_support_revenue(support, base_churn_rate, customers, base_revenue)  # Calculate revenue from support
        
        cumulative_revenue += monthly_revenue
        monthly_revenues.append(monthly_revenue)
        account_manager_revenues.append(manager_revenue)
        new_business_revenues.append(new_business_revenue)
        # support_revenues.append(support_revenue)
        cumulative_revenues.append(cumulative_revenue)

        # print(f"Month {month} - Monthly Revenue: ${monthly_revenue}, Account Manager Revenue: ${manager_revenue}, Cumulative Revenue: ${cumulative_revenue}")
        print(f"Month {month} - Monthly Revenue: ${monthly_revenue}, Cumulative Revenue: ${cumulative_revenue}, New Business Revenue: ${new_business_revenue}")

    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(monthly_revenues, label='Total Monthly Revenue')
    plt.plot(cumulative_revenues, label='Cumulative Revenue')
    plt.xlabel('Month')
    plt.ylabel('Revenue ($)')
    plt.title('Total and Cumulative Revenue')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(account_manager_revenues, label='Monthly Revenue from Account Managers', color='orange')
    plt.plot(new_business_revenues, label='Monthly Revenue from New Business Acquisition', color='blue')
    # plt.plot(support_revenues, label='Revenue from Support', color='red')
    plt.xlabel('Month')
    plt.ylabel('Revenue ($)')
    plt.title('Revenue from Each Role')
    plt.legend()

    plt.tight_layout()
    plt.show()

run_simulation()
