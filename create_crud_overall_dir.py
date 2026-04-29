
import os

dir_to_create = "C:/Users/ruhan/Faculty_appraisal/src/crud/overall"

if not os.path.exists(dir_to_create):
    try:
        os.makedirs(dir_to_create)
        print(f"Successfully created directory: {dir_to_create}")
    except OSError as e:
        print(f"Error creating directory {dir_to_create}: {e}")
else:
    print(f"Directory already exists: {dir_to_create}")
