import os
import statistics
import pandas as pd
from exploration import create_text_dict
from customer import *


base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_path = os.path.join(base_path, 'output')

text_ele = create_text_dict()


# Storing all the customer details for future use
customer_names = get_customer_names()
customer_emails = get_customer_email()
customer_add_line1 = get_customer_add1()
customer_add_line2 = get_customer_add2()
customer_phone_nos = get_customer_phone_no()


# To get invoice due dates
def get_invoice_due_date():
    due_dates = [None] * 100    # List of size 100 to store due dates

    # Iterating over all the text elements from all the structured json files
    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]): 
            if 'Due date' in item:                  # If the text element contains 'Due date' then  
                due_dates[i] = item.split(" ")[2]   # actual date will follow 'Due' and 'date' and be the 3rd word in that text
                
                break
    
    return due_dates


invoice_due_dates = get_invoice_due_date()


# To get invoice issue dates
def get_invoice_issue_date():
    issue_dates = [None] * 100     # List of size 100 to store issue dates

    # Iterating over all the text elements from all the structured json files
    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]): 
            if 'Issue date' in item:
                if item.split(" ")[-2] == 'date':                          # If the text element ends with word 'date' 
                    issue_dates[i] = text_ele[i][j + 1].split(" ")[0]      # date will be in the beginning of the next text element
                
                else:                                                      # If 'date' is not in the end
                    issue_dates[i] = item.split(" ")[-2]                   # date will be at the end of that text element

                break
    
    return issue_dates


invoice_issue_dates = get_invoice_issue_date()


# To get the invoice tax rate
def get_invoice_tax():
    invoice_tax = [None] * 100        # List of size 100 to store tax rates

    # Iterating over all the text elements from all the structured json files
    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]): 
            if 'Tax' in item:
                # print(i, item + '->' +  text_ele[i][j + 1] + '-->' +  text_ele[i][j + 2])

                # If the word 'Tax' and tax rate both are in the different text element
                if len(item.split(" ")) == 3:

                    # If the next text element contains PAYMENT amount
                    if text_ele[i][j + 1][0] == '$':
                        invoice_tax[i] = int(text_ele[i][j + 2].split(" ")[0])
                    
                    # If the next text element contains tax rate
                    else:
                        invoice_tax[i] = int(text_ele[i][j + 1].split(" ")[0])
                
                # If the word 'Tax' and tax rate both are in the same text element
                else:                   
                    invoice_tax[i] = int(text_ele[i][j].split(" ")[2])
    
    # If someones tax rate can't be extracted then assign it the most frequent tax rate
    if invoice_tax.count(None) > 0:
        for i in range(len(invoice_tax)):
            if invoice_tax[i] == None:
                invoice_tax[i] = statistics.mode(invoice_tax)

    return invoice_tax


invoice_tax_rates = get_invoice_tax()
# print(invoice_tax_rates)


# To get invoice number
def get_invoice_number():
    invoice_nos = [None] * 100      # List of size 100 to store invoice number

    # Iterating over all the text elements from all the structured json files
    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]):
            if '#' in item:
                # print(i, item + '->' + text_ele[i][j + 1] + '-->' + text_ele[i][j + 2])

                # If the invoice no. is not in respective text element. Fetch it from the next text element.
                if len(item.split(" ")) == 2:
                    invoice_nos[i] = text_ele[i][j + 1].split(" ")[0]
                
                # If the invoice no. is in respective text element.
                else:
                    invoice_nos[i] = text_ele[i][j].split(" ")[1]

    return invoice_nos                

invoice_numbers = get_invoice_number()


# To get invoice description
def get_invoice_description():
    invoice_desc = [None] * 100      # List of size 100 to store invoice description

    # Iterating over the files in tables folder from TextTableWithTableStructure of each PDF file
    for i, data in enumerate(os.listdir(output_path)):
        tables_path = os.path.join(output_path, f'TextTableWithTableStructure_{i}/tables')

        # If tables folder contains 8 files 
        if len(os.listdir(tables_path)) == 8:
            fileout_path = os.path.join(tables_path, 'fileoutpart0.csv')   # fileoutpart0.csv contains details of the description
            details_df = pd.read_csv(fileout_path)     
            
            detail = ""

            # If there is only column then it only contains description
            if len(details_df.columns) == 1:
                if details_df.columns[0] == 'DETAILS  ':

                    # Iterate over all the rows to get the full description
                    for d in details_df['DETAILS  '].tolist():
                        detail += str(d)[0:-1]
                
                # If there isn't a column named 'DETAILS' then a part of description is acting as column name
                else:
                    col_name = str(details_df.columns[0])
                    detail = col_name[0:-1]        # column name is used to initialize the variable contaning description
                    
                    # Iterate over all the rows to get the full description
                    for d in details_df[col_name].tolist():
                        detail += str(d)[0:-1]
                    
            
            # elif len(details_df.columns) == 2:
            #     for d in details_df['DETAILS  '].tolist():
            #         detail += str(d)[0:-1]
                
            # If there are more than 1 columns then iterate over 'DETAILS' column
            else:
                for d in details_df['DETAILS  '].tolist():
                    detail += str(d)[0:-1]
                
            
            invoice_desc[i] = detail

    # If tables folder have less than 8 files iterate over all the text elements from all the structured json files
    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]):
            if invoice_desc[i] == None:
                details = ""

                # If description is on the same line as 'DETAILS'
                if "DETAILS" in item and len(item.split(" ")) > 2:
                    details = item[8:]
                    details = details.replace("PAYMENT", "")
                    details = details.strip()

                    invoice_desc[i] = details
                    
                    
                # If the text element only contains "DETAILS" and "PAYMENT" in next element, description will start after "PAYMENT" element
                elif "DETAILS" in item and "PAYMENT" in text_ele[i][j + 1]:
                    k = j + 2

                    # Iterate till text element containing 'Due' is reached 
                    while 'Due' not in text_ele[i][k]:
                        details += text_ele[i][k]
                        k += 1

                    # Filtering the details
                    details = details.replace("PAYMENT", "")    # Remove the word "PAYMENT"
                    details = details.replace(customer_names[i], "")    # Remove customer names
                    details = details.replace(customer_phone_nos[i], "")    # Remove customer phone nos.
                    details = re.sub(r'\$\d+', "", details)    # Remove any amount by removing words starting with '$'
                    details = re.sub(r'\S+[@.]\S+', "", details)    # Remove email address by removing words containing '@', '.'
                    details = details.replace(customer_add_line1[i], "")    # Remove customer address line 1
                    details = details.replace(customer_add_line2[i], "")    # Remove customer address line 2
                    details = details.strip()    # Remove empty spaces from start and end

                    invoice_desc[i] = details

                    
                # If the text element only contains "DETAILS"
                elif "DETAILS" in item:
                    k = j + 1

                    # Iterate till text element containing 'Due' is reached 
                    while 'Due' not in text_ele[i][k]:
                        details += text_ele[i][k]
                        k += 1

                    # Filtering the details
                    details = details.replace("PAYMENT", "")    # Remove the word "PAYMENT"
                    details = details.replace(customer_names[i], "")    # Remove customer names
                    details = details.replace(customer_phone_nos[i], "")    # Remove customer phone nos.
                    details = re.sub(r'\$\d+', "", details)    # Remove any amount by removing words starting with '$'
                    details = re.sub(r'\S+[@.]\S+', "", details)    # Remove email address by removing words containing '@', '.'
                    details = details.replace(customer_add_line1[i], "")    # Remove customer address line 1
                    details = details.replace(customer_add_line2[i], "")    # Remove customer address line 2
                    details = details.strip()    # Remove empty spaces from start and end

                    invoice_desc[i] = details
                
    
    return invoice_desc
                           

invoice_desc = get_invoice_description()


# To get invoice bill details name, quantity and rate
def get_invoice_bill_details():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_path, 'output')

    item_details = []    # List to store item details

    # Iterate over the tables from all the TextTableWithTableStructure outputs
    for i, data in enumerate(os.listdir(output_path)):
        tables_path = os.path.join(output_path, f'TextTableWithTableStructure_{i}/tables')

        fileout_path = ""

        # For tables directory with 4 files: fileoutpart2.csv contains the details
        if len(os.listdir(tables_path)) == 4: 
            fileout_path = os.path.join(tables_path, f'fileoutpart{2}.csv')
        
        # For tables directory with 6 files: fileoutpart2.csv contains the details
        if len(os.listdir(tables_path)) == 6: 
            fileout_path = os.path.join(tables_path, f'fileoutpart{2}.csv')

        # For tables directory with 8 files: fileoutpart4.csv contains the details
        if len(os.listdir(tables_path)) == 8: 
            fileout_path = os.path.join(tables_path, f'fileoutpart{4}.csv')
        
        item_df = pd.read_csv(fileout_path, header=None)

        # For tables with 6 files: if the dataframe only has column names, get the next fileoutpart file for item details
        if 'ITEM' in item_df.iloc[0,0]:
            fileout_path = os.path.join(tables_path, f'fileoutpart{4}.csv')
            item_df = pd.read_csv(fileout_path, header=None)

        # Dictionary mapping Bill detail attributes to their values in form of a list
        item_dict = dict()

        # Fetch the name, quantity and rates from the dataframe and add it 
        for j in range(len(item_df)):
            item_dict.setdefault("Invoice__BillDetails__Name", []).append(item_df.iloc[j,0])
            item_dict.setdefault("Invoice__BillDetails__Quantity", []).append(item_df.iloc[j,1])
            item_dict.setdefault("Invoice__BillDetails__Rate", []).append(item_df.iloc[j,2])

        item_details.append(item_dict)

    
    return item_details



invoice_bill_details = get_invoice_bill_details()