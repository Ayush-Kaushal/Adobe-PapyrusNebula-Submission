from customer import *
from business import *
from invoice import *

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

column_names = ["Bussiness__City", "Bussiness__Country", "Bussiness__Description", "Bussiness__Name", "Bussiness__StreetAddress", 
                "Bussiness__Zipcode", "Customer__Address__line1", "Customer__Address__line2", "Customer__Email", "Customer__Name", 
                "Customer__PhoneNumber", "Invoice__BillDetails__Name", "Invoice__BillDetails__Quantity", "Invoice__BillDetails__Rate", 
                "Invoice__Description", "Invoice__DueDate", "Invoice__IssueDate", "Invoice__Number", "Invoice__Tax"]

ExtractedData_df = pd.DataFrame(columns=column_names)


business_details = get_business_details()

customer_add_line1 = get_customer_add1()
customer_add_line2 = get_customer_add2()
customer_emails = get_customer_email()
customer_names = get_customer_names()
customer_phone_nos = get_customer_phone_no()

invoice_bill_details = get_invoice_bill_details()
invoice_desc = get_invoice_description()
invoice_due_dates = get_invoice_due_date()
invoice_issue_dates = get_invoice_issue_date()
invoice_numbers = get_invoice_number()
invoice_tax_rates = get_invoice_tax()

for i in range(100):

    Bussiness__City = business_details["Bussiness__City"][i]
    Bussiness__Country = business_details["Bussiness__Country"][i]
    Bussiness__Description = business_details["Bussiness__Description"][i]
    Bussiness__Name = business_details["Bussiness__Name"][i]
    Bussiness__StreetAddress = business_details["Bussiness__StreetAddress"][i]
    Bussiness__Zipcode = business_details["Bussiness__Zipcode"][i]

    Customer__Address__line1 = customer_add_line1[i]
    Customer__Address__line2 = customer_add_line2[i]
    Customer__Email = customer_emails[i]
    Customer__Name = customer_names[i]
    Customer__PhoneNumber = customer_phone_nos[i]

    Invoice__Description = invoice_desc[i]
    Invoice__DueDate = invoice_due_dates[i]
    Invoice__IssueDate = invoice_issue_dates[i]
    Invoice__Number = invoice_numbers[i]
    Invoice__Tax = invoice_tax_rates[i]

    for j in range(int(len(invoice_bill_details[i]["Invoice__BillDetails__Name"]))):

        Invoice__BillDetails__Name = invoice_bill_details[i]["Invoice__BillDetails__Name"][j]
        Invoice__BillDetails__Quantity = invoice_bill_details[i]["Invoice__BillDetails__Quantity"][j]
        Invoice__BillDetails__Rate = invoice_bill_details[i]["Invoice__BillDetails__Rate"][j]


        new_row = [{"Bussiness__City": Bussiness__City, 
              "Bussiness__Country": Bussiness__Country, 
              "Bussiness__Description": Bussiness__Description, 
              "Bussiness__Name": Bussiness__Name, 
              "Bussiness__StreetAddress": Bussiness__StreetAddress, 
              "Bussiness__Zipcode": Bussiness__Zipcode, 
              "Customer__Address__line1": Customer__Address__line1, 
              "Customer__Address__line2": Customer__Address__line2, 
              "Customer__Email": Customer__Email, 
              "Customer__Name": Customer__Name, 
              "Customer__PhoneNumber": Customer__PhoneNumber, 
              "Invoice__BillDetails__Name": Invoice__BillDetails__Name, 
              "Invoice__BillDetails__Quantity": Invoice__BillDetails__Quantity, 
              "Invoice__BillDetails__Rate": Invoice__BillDetails__Rate, 
              "Invoice__Description": Invoice__Description, 
              "Invoice__DueDate": Invoice__DueDate, 
              "Invoice__IssueDate": Invoice__IssueDate, 
              "Invoice__Number": Invoice__Number, 
              "Invoice__Tax": Invoice__Tax
              }]
        
        new_row_df = pd.DataFrame(new_row, columns=column_names)
        
        ExtractedData_df = pd.concat([ExtractedData_df, new_row_df], ignore_index=True)        



print(ExtractedData_df.shape)

# ExtractedData_Path = os.path.join(base_path, 'ExtractedData/ExtractedData.csv')

# ExtractedData_df.to_csv(ExtractedData_Path, index=False)


