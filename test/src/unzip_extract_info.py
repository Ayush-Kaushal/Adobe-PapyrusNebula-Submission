import os
import shutil

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# unziping all the outputs
for i in range(100):
    zip_file_path = base_path + f"/output/ExtractTextTableWithTableStructure{i}.zip"
    extract_path = base_path + f"/output/TextTableWithTableStructure_{i}"
    shutil.unpack_archive(zip_file_path, extract_path)

    # removing the zip folders
    os.remove(base_path + f"/output/ExtractTextTableWithTableStructure{i}.zip")

    
