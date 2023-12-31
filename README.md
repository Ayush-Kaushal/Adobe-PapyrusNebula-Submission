﻿# Adobe-PapyrusNebula-Submission
This project contains the submission for Adobe PapyrusNebula Hackathon. The required __ExtractedData.csv__ file is in the following location: ```/test/ExtractedData/ExtractedData.csv```

## Getting Started

### Prerequisites
- Python : Version 3.6 or above. Python installation instructions can be found [here](https://www.python.org/).

### Installation
To run the code on your machine and generate the output follow the steps:  

1. Open terminal in the folder you want to clone the project and type:  
```https://github.com/Ayush-Kaushal/Adobe-PapyrusNebula-Submission.git```

2. Install the project dependencies:  
```pip install -r requirements.txt```

## Project Structure
- ```/test``` directory consists all the necessary files and folders in respect to the hackathon.
- ```/test/resources``` directory contains all the input PDF files for testing.
- ```/test/src``` directory contains all source codes.
- ```/test/output``` directory contains the extracted inforamtion from the all the input PDF files.
- ```/test/ExtractedData``` directory contains the submission file ```ExtractedData.csv```.
- ```/test/src/extract_info.py``` to extract text and table information from the pdf file.
- ```/test/src/unzip_extract_info.py``` to unzip the extracted information and store it the ```output``` directory.
- ```/test/src/exploration.py``` to extract the text elements from the structured data.
- ```/test/src/business.py``` file contains the code to get all the necessary details about the business.
- ```/test/src/customer.py``` file contains the code to get all the necessary details about the customer.
- ```/test/src/invoice.py``` file contains the code to get all the necessary details about the invoice bill.
- ```/test/src/final_output.py``` conatins the code that generates the ```ExtractedData.csv``` file for submission.


## Running the project
To run the project, run the python files in ```/test/src``` directory in the following order:

1. ```/test/src/extract_info.py```
2. ```/test/src/unzip_extract_info.py```
3. ```/test/src/exploration.py```
4. ```/test/src/customer.py```
5. ```/test/src/invoice.py```
6. ```/test/src/business.py```
