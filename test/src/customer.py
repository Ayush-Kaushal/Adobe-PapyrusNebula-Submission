import re
from exploration import create_text_dict

text_ele = create_text_dict()

# To get the customer phone numbers 
def get_customer_phone_no():
    phone_nos = []   # list to store phone nos.
    phone_regex = "\d{3}[-]\d{3}[-]\d{4}"  # regular expression for phone no.

    # Iterating over all the text elements from all the structured json files
    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]):    
            match = re.search(phone_regex, item)   
            
            # If phone no. is present in text element 
            if match != None:
                phone_nos.append(match.group(0))   # match.group() returns the matched substring i.e. phone no.
                break
    
    return phone_nos

        
customer_phone_nos = get_customer_phone_no()

# print(customer_phone_nos)


# To get the customer email ids
def get_customer_email():
    emails = []    # list to store email

    # Iterating over all the text elements from all the structured json files
    for i in range(len(text_ele)):
        email = ""

        for j, item in enumerate(text_ele[i]):  
            if '@' in item:
                for s in item.split(' '):
                    if '@' in s:
                        email = s
                        break
                
                # Some information may be lost as email might be broken in 2 lines so attach domain name manually
                domain = email.split('@')[1]
                if domain[0] == 'y':
                    domain = 'yahoo.com'
                elif domain[0] == 'g':
                    domain = 'gmail.com'
                elif domain[0] == 'h':
                    domain = 'hotmail.com'
                # else:
                #     print(domain[0])
                
                email = email.split('@')[0] + '@' + domain
                
                emails.append(email)

                break
                
        
    return emails

customer_emails = get_customer_email()

# print(len(customer_emails))



# To get customer customer names
def get_customer_names():
    first_names = []   # List to store first names

    # Get the first names from the respective email ids. 
    for email in customer_emails:
        mail = email.replace('_', ' ')     # Replace '_' in emails with ' '
        mail = re.sub(r"\d", " ", mail)    # Replace numbers in emails with ' '
        first_names.append(re.findall(r"[\w']+", mail)[0])     # Select the 1st string with word characters
    
    full_names = []    # List to store first names

    # Iterating over all the text elements from all the structured json files
    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]):

            # Find the element with the first name
            # Since the name in PDF file has its own line we can select the 1st two string in that text element to get full name
            if first_names[i] in item:
                full_names.append(item.split(' ')[0] + ' ' + item.split(' ')[1])
                break
    
    return full_names

customer_names = get_customer_names()


# To get address line 1 
def get_customer_add1():
    add_line_1 = [None] * 100    # List of size 100 to store address line 1

    phone_regex = "\d{3}[-]\d{3}[-]\d{4}"   # Regular expression to match phone no.

    # Iterating over all the text elements from all the structured json files
    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]):    
            # Search for phone no. in text element
            match = re.search(phone_regex, item)

            if match != None:
                s = " "
                
                # Street address starts with nos. and is proceeded with phone no. Check the next element for nos.
                if text_ele[i][j + 1][0].isdigit():
                    add_line_1[i] = s.join(text_ele[i][j + 1].split(' ')[:3])

                
                else:
                    # Elements between phone no. and address line 1 might be filled other information
                    if len(text_ele[i][j].split(' ')) == 2:
                        add_line_1[i] = s.join(text_ele[i][j + 3].split(' ')[:3])
                    
                    # Element containing phone no. also contains address line 1
                    else: 
                        add_line_1[i] = s.join(text_ele[i][j][match.end() + 1 : ].split(" ")[:3])


                break
    
    return add_line_1


customer_add_line1 = get_customer_add1()
# print(customer_add_line1)


# Dictionary that maps phone nos. to address line 1
phone_adds1_dict = {}
for i in range(len(customer_phone_nos)):
    phone_adds1_dict[customer_phone_nos[i]] = customer_add_line1[i]


# Dictionary that maps phone nos. to all the indices with that phone no.
phone_index_dict = dict()
for i in range(len(customer_phone_nos)):
    phone_index_dict.setdefault(customer_phone_nos[i], []).append(i)


# To get customer address line 2
def get_customer_add2():
    add_line_2 = [None] * 100     # List of size 100 to store address line 2

    s = " "

   # Iterating over all the text elements from all the structured json files 
    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]):   

            # Search the text element for address line 1 of the respective customer 
            if customer_add_line1[i] in item and add_line_2[i] == None:
                if text_ele[i][j + 1][0].isupper() :     # Address starts with a captial letter

                    # Put the current address line 2 to all indices shared by the phone no. of the given customer
                    for idx in phone_index_dict[customer_phone_nos[i]]:
                        add_line_2[idx] = s.join(text_ele[i][j + 1].split(' ')[0:-1])

                break
    
    return add_line_2


customer_add_line2 = get_customer_add2()

