
import os
import shutil

dir_to_remove = "C:/Users/ruhan/Faculty_appraisal/src/api/v1/endpoints"

if os.path.exists(dir_to_remove):
    try:
        shutil.rmtree(dir_to_remove)
        print(f"Successfully removed directory: {dir_to_remove}")
    except OSError as e:
        print(f"Error removing directory {dir_to_remove}: {e}")
else:
    print(f"Directory not found: {dir_to_remove}")
