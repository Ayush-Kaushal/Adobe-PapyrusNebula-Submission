import re
from exploration import create_text_dict

text_ele = create_text_dict()


# To get all the business related information
def get_business_details():
    business_dict = dict()

    # To get the business name grab the first text element
    for i in range(len(text_ele)):
        business_dict.setdefault("Bussiness__Name", []).append(text_ele[i][0].strip())  


    # To get the business address
    for i in range(len(text_ele)):
        
        # If street, city and country all are in the 2nd text element ans PIN code is in next text element
        if re.search(r'\d+', text_ele[i][2]) != None:
            business_dict.setdefault("Bussiness__StreetAddress", []).append(text_ele[i][1].split(",")[0].strip())
            business_dict.setdefault("Bussiness__City", []).append(text_ele[i][1].split(",")[1].strip())
            business_dict.setdefault("Bussiness__Country", []).append(text_ele[i][1].split(",")[2] + ", " + text_ele[i][1].split(",")[3].strip())
            business_dict.setdefault("Bussiness__Zipcode", []).append(text_ele[i][2].strip())

        # If street, city, country and PIN code are in consecutive text elements 
        else:
            business_dict.setdefault("Bussiness__StreetAddress", []).append(text_ele[i][1].split(",")[0].strip())
            business_dict.setdefault("Bussiness__City", []).append(text_ele[i][1].split(",")[1].strip())
            business_dict.setdefault("Bussiness__Country", []).append(text_ele[i][2].strip())
            business_dict.setdefault("Bussiness__Zipcode", []).append(text_ele[i][3].strip())
    

    # Iterating over all the text elements from all the structured json files
    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]):

            # To get the business description grab the text element just before 'BILL TO' text element
            if 'BILL TO' in item:
                business_dict.setdefault("Bussiness__Description", []).append(text_ele[i][j - 1].strip())

    return business_dict


business_details = get_business_details() 

