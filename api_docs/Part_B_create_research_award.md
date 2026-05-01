# Create Research Award

**Endpoint Name:** Create Research Award  
**URL Path:** `/api/v1/part-b/research-awards`  
**Method:** `POST`

## Description
Adds a new research award or recognition received by the faculty.

## Access Control
- **Role Required:** `faculty`.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**
  - `award_name` (str): Name of the award.
  - `award_date` (date): Date of receiving the award.
  - `awarding_agency` (str): Organization that gave the award.
  - `level` (str): International/National/State level.
  - `department` (str, optional): Faculty's department.
  - `file` (file, optional): PDF certificate of the award.

## Response Data
- **Code:** `201 Created`
- **Fields:** Standard Research Award fields.
