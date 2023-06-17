import os
import statistics
import pandas as pd
from exploration import create_text_dict
from customer import *


base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_path = os.path.join(base_path, 'output')

text_ele = create_text_dict()

customer_names = get_customer_names()
customer_emails = get_customer_email()
customer_add_line1 = get_customer_add1()
customer_add_line2 = get_customer_add2()
customer_phone_nos = get_customer_phone_no()

def get_invoice_due_date():
    due_dates = [None] * 100

    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]): 
            if 'Due date' in item:
                due_dates[i] = item.split(" ")[2]
                # print(due_dates[i])

                break
    
    return due_dates


invoice_due_dates = get_invoice_due_date()


def get_invoice_issue_date():
    issue_dates = [None] * 100

    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]): 
            if 'Issue date' in item:
                # issue_dates[i] = item.split(" ")[2]
                # print(i, item + '--->' + text_ele[i][j + 1])
                if item.split(" ")[-2] == 'date':
                    issue_dates[i] = text_ele[i][j + 1].split(" ")[0]
                
                else:
                    issue_dates[i] = item.split(" ")[-2]

                break
    
    return issue_dates


invoice_issue_dates = get_invoice_issue_date()



def get_invoice_tax():
    invoice_tax = [None] * 100

    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]): 
            if 'Tax' in item:
                # print(i, item + '->' +  text_ele[i][j + 1] + '-->' +  text_ele[i][j + 2])
                if len(item.split(" ")) == 3:
                    if text_ele[i][j + 1][0] == '$':
                        invoice_tax[i] = int(text_ele[i][j + 2].split(" ")[0])
                    else:
                        invoice_tax[i] = int(text_ele[i][j + 1].split(" ")[0])
                
                else:
                    invoice_tax[i] = int(text_ele[i][j].split(" ")[2])

    if invoice_tax.count(None) > 0:
        for i in range(len(invoice_tax)):
            if invoice_tax[i] == None:
                invoice_tax[i] = statistics.mode(invoice_tax)

    return invoice_tax


invoice_tax_rates = get_invoice_tax()
# print(invoice_tax_rates)



def get_invoice_number():
    invoice_nos = [None] * 100

    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]):
            if '#' in item:
                # print(i, item + '->' + text_ele[i][j + 1] + '-->' + text_ele[i][j + 2])

                if len(item.split(" ")) == 2:
                    invoice_nos[i] = text_ele[i][j + 1].split(" ")[0]
                else:
                    invoice_nos[i] = text_ele[i][j].split(" ")[1]

    return invoice_nos                

invoice_numbers = get_invoice_number()



def get_invoice_description():
    invoice_desc = [None] * 100

    for i, data in enumerate(os.listdir(output_path)):
        tables_path = os.path.join(output_path, f'TextTableWithTableStructure_{i}/tables')

        if len(os.listdir(tables_path)) == 8:
            fileout_path = os.path.join(tables_path, 'fileoutpart0.csv')
            details_df = pd.read_csv(fileout_path)
            
            detail = ""
            if len(details_df.columns) == 1:
                if details_df.columns[0] == 'DETAILS  ':
                    for d in details_df['DETAILS  '].tolist():
                        detail += str(d)[0:-1]
                    #print(detail)
                
                else:
                    col_name = str(details_df.columns[0])
                    detail = col_name[0:-1]
                    for d in details_df[col_name].tolist():
                        detail += str(d)[0:-1]
                    #print(detail)

            elif len(details_df.columns) == 2:
                for d in details_df['DETAILS  '].tolist():
                    detail += str(d)[0:-1]
                #print(detail)

            else:
                for d in details_df['DETAILS  '].tolist():
                    detail += str(d)[0:-1]
                #print(detail)
            
            invoice_desc[i] = detail
            # print(invoice_desc[i])

    
    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]):
            if invoice_desc[i] == None:
                details = ""

                if "DETAILS" in item and len(item.split(" ")) > 2:
                    details = item[8:]
                    details = details.replace("PAYMENT", "")
                    details = details.lstrip()
                    details = details.rstrip()

                    invoice_desc[i] = details

                    # print(i, item[8:])
                    

                elif "DETAILS" in item and "PAYMENT" in text_ele[i][j + 1]:
                    k = j + 2
                    while 'Due' not in text_ele[i][k]:
                        details += text_ele[i][k]
                        k += 1

                    details = details.replace("PAYMENT", "")
                    details = details.replace(customer_names[i], "")
                    details = details.replace(customer_phone_nos[i], "")
                    details = re.sub(r'\$\d+', "", details)
                    details = re.sub(r'\S+[@.]\S+', "", details)
                    details = details.replace(customer_add_line1[i], "")
                    details = details.replace(customer_add_line2[i], "")
                    details = details.lstrip()
                    details = details.rstrip()

                    invoice_desc[i] = details

                    # print(i, details)
                    

                elif "DETAILS" in item:
                    k = j + 1
                    while 'Due' not in text_ele[i][k]:
                        details += text_ele[i][k]
                        k += 1


                    details = details.replace("PAYMENT", "")
                    details = details.replace(customer_names[i], "")
                    details = details.replace(customer_phone_nos[i], "")
                    details = re.sub(r'\$\d+', "", details)
                    details = re.sub(r'\S+[@.]\S+', "", details)
                    details = details.replace(customer_add_line1[i], "")
                    details = details.replace(customer_add_line2[i], "")
                    details = details.lstrip()
                    details = details.rstrip()

                    invoice_desc[i] = details

                    # print(i, details)
                
                
                # print(i, details)
    
    return invoice_desc
                           

# invoice_desc = get_invoice_description()
# print(invoice_desc)
# print(invoice_desc.count(None))

# for ele in text_ele[22]:
#     print(ele)



def get_invoice_bill_details():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_path, 'output')

    item_details = []

    for i, data in enumerate(os.listdir(output_path)):
        tables_path = os.path.join(output_path, f'TextTableWithTableStructure_{i}/tables')

        fileout_path = ""
        if len(os.listdir(tables_path)) == 4: 
            fileout_path = os.path.join(tables_path, f'fileoutpart{2}.csv')
            
        if len(os.listdir(tables_path)) == 6: 
            fileout_path = os.path.join(tables_path, f'fileoutpart{2}.csv')

        if len(os.listdir(tables_path)) == 8: 
            fileout_path = os.path.join(tables_path, f'fileoutpart{4}.csv')
        
        item_df = pd.read_csv(fileout_path, header=None)
        if 'ITEM' in item_df.iloc[0,0]:
            fileout_path = os.path.join(tables_path, f'fileoutpart{4}.csv')
            item_df = pd.read_csv(fileout_path, header=None)

        
        item_dict = dict()
        for j in range(len(item_df)):
            item_dict.setdefault("Invoice__BillDetails__Name", []).append(item_df.iloc[j,0])
            item_dict.setdefault("Invoice__BillDetails__Quantity", []).append(item_df.iloc[j,1])
            item_dict.setdefault("Invoice__BillDetails__Rate", []).append(item_df.iloc[j,2])

        item_details.append(item_dict)

        # print(i, len(item_df))
        # print('-------------------------------------------------------------')
    
    return item_details



invoice_bill_details = get_invoice_bill_details()
# print(len(invoice_bill_details[]))