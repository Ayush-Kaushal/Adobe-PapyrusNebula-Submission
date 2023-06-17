import os
import json
import pandas as pd

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

output_path = os.path.join(base_path, 'output')


####################### Exploring structuredData file ############################

# Extracting all the text elements from the structuredData file

def create_text_dict():
    text_ele = {}

    for i, data in enumerate(os.listdir(output_path)):
        # tables_path = os.path.join(output_path, f'TextTableWithTableStructure_{i}/tables')
        json_path = os.path.join(output_path, f'TextTableWithTableStructure_{i}/structuredData.json')

        with open(json_path, 'r') as f:
            info_dict = json.load(f)

        lis = []
        for j, tag in enumerate(info_dict['elements']):
            if tag.get('Text') == None:
                continue
        
            lis.append(tag['Text'])
        
        text_ele[i] = lis
    
    return text_ele


text_ele = create_text_dict()


   