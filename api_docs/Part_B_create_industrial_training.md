# Create Industrial Training

**Endpoint Name:** Create Industrial Training  
**URL Path:** `/api/v1/part-b/industrial-training`  
**Method:** `POST`

## Description
Adds a new record for industrial training or internship completed by the faculty member.

## Access Control
- **Role Required:** `faculty`.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**
  - `company_industry` (str): Name of the company/industry.
  - `duration_days` (int): Duration of the training in days.
  - `nature_of_training` (str): Brief about what the training was about.
  - `department` (str, optional): Faculty's department.
  - `file` (file, optional): PDF certificate of completion.

## Response Data
- **Code:** `201 Created`
- **Fields:** Standard Industrial Training fields.
