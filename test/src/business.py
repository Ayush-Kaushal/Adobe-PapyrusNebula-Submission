import re
from exploration import create_text_dict

text_ele = create_text_dict()

def get_business_details():
    business_dict = dict()

    for i in range(len(text_ele)):
        business_dict.setdefault("Bussiness__Name", []).append(text_ele[i][0].strip())


    for i in range(len(text_ele)):
        
        if re.search(r'\d+', text_ele[i][2]) != None:
            business_dict.setdefault("Bussiness__StreetAddress", []).append(text_ele[i][1].split(",")[0].strip())
            business_dict.setdefault("Bussiness__City", []).append(text_ele[i][1].split(",")[1].strip())
            business_dict.setdefault("Bussiness__Country", []).append(text_ele[i][1].split(",")[2] + ", " + text_ele[i][1].split(",")[3].strip())
            business_dict.setdefault("Bussiness__Zipcode", []).append(text_ele[i][2].strip())

        else:
            business_dict.setdefault("Bussiness__StreetAddress", []).append(text_ele[i][1].split(",")[0].strip())
            business_dict.setdefault("Bussiness__City", []).append(text_ele[i][1].split(",")[1].strip())
            business_dict.setdefault("Bussiness__Country", []).append(text_ele[i][2].strip())
            business_dict.setdefault("Bussiness__Zipcode", []).append(text_ele[i][3].strip())
    


    for i in range(len(text_ele)):
        for j, item in enumerate(text_ele[i]):
            if 'BILL TO' in item:
                business_dict.setdefault("Bussiness__Description", []).append(text_ele[i][j - 1].strip())

    return business_dict


# business_details = get_business_details() 

# print(len(business_details["Bussiness__StreetAddress"]), len(business_details["Bussiness__City"]), len(business_details["Bussiness__Country"]))
# print(len(business_details["Bussiness__Zipcode"]), len(business_details["Bussiness__Name"]), len(business_details["Bussiness__Description"]))

# print(business_details)
