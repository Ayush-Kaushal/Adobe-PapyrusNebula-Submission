import re
from exploration import create_text_dict

text_ele = create_text_dict()


def get_customer_phone_no():
    phone_nos = []
    phone_regex = "\d{3}[-]\d{3}[-]\d{4}"

    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]):    
            match = re.search(phone_regex, item)
            if match != None:
                phone_nos.append(match.group(0))
                break
    
    return phone_nos

        
customer_phone_nos = get_customer_phone_no()

# print(customer_phone_nos)

def get_customer_email():
    emails = []

    for i in range(len(text_ele)):
        email = ""
        for j, item in enumerate(text_ele[i]):  
            if '@' in item:
                for s in item.split(' '):
                    if '@' in s:
                        email = s
                        break
                #print(i, email)

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
                #print(i, email)
                emails.append(email)

                break
                
        
    return emails

customer_emails = get_customer_email()

# print(len(customer_emails))




def get_customer_names():
    first_names = []
    for email in customer_emails:
        mail = email.replace('_', ' ')
        mail = re.sub(r"\d", " ", mail)
        first_names.append(re.findall(r"[\w']+", mail)[0])
    
    full_names = []
    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]):
            if first_names[i] in item:
                full_names.append(item.split(' ')[0] + ' ' + item.split(' ')[1])
                break
    
    return full_names

customer_names = get_customer_names()



def get_customer_add1():
    add_line_1 = [None] * 100

    phone_regex = "\d{3}[-]\d{3}[-]\d{4}"

    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]):    
            match = re.search(phone_regex, item)
            if match != None:
                s = " "

                if text_ele[i][j + 1][0].isdigit():
                    # print(i, text_ele[i][j + 1].split(' ')[0])
                    add_line_1[i] = s.join(text_ele[i][j + 1].split(' ')[:3])

                else:
                    if len(text_ele[i][j].split(' ')) == 2:
                        # print(i, text_ele[i][j + 3])
                        add_line_1[i] = s.join(text_ele[i][j + 3].split(' ')[:3])

                    else: 
                        # print(i, text_ele[i][j] + '-->' + text_ele[i][j][match.end() + 1 : ])
                        add_line_1[i] = s.join(text_ele[i][j][match.end() + 1 : ].split(" ")[:3])
                        # print(i, text_ele[i][j][match.end() + 1 : ].split(" ")[:3])


                break
    
    return add_line_1


customer_add_line1 = get_customer_add1()
# print(customer_add_line1)

phone_adds1_dict = {}
for i in range(len(customer_phone_nos)):
    phone_adds1_dict[customer_phone_nos[i]] = customer_add_line1[i]

# print(len(phone_adds1_dict))


phone_index_dict = dict()

for i in range(len(customer_phone_nos)):
    phone_index_dict.setdefault(customer_phone_nos[i], []).append(i)

# print(phone_index_dict)
# print(len(phone_index_dict))

def get_customer_add2():
    add_line_2 = [None] * 100

    s = " "
    
    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]):    
            if customer_add_line1[i] in item and add_line_2[i] == None:
                if text_ele[i][j + 1][0].isupper() :
                    for idx in phone_index_dict[customer_phone_nos[i]]:
                        add_line_2[idx] = s.join(text_ele[i][j + 1].split(' ')[0:-1])

                # print(i, text_ele[i][j + 1], text_ele[i][j + 1][0].isupper())
                break
    
    return add_line_2


customer_add_line2 = get_customer_add2()
# print(customer_add_line2)








# for ele in text_ele[94]:
#     print(ele)