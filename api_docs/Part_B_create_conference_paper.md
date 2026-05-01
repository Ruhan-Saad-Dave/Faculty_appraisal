# Create Conference Paper

**Endpoint Name:** Create Conference Paper  
**URL Path:** `/api/v1/part-b/conferences`  
**Method:** `POST`

## Description
Adds a new record for a paper presented in a conference or seminar.

## Access Control
- **Role Required:** `faculty`.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**
  - `event_title` (str): Title of the conference/seminar.
  - `event_date` (date): Date of the event.
  - `activity_type` (str): Type of presentation (Oral/Poster, etc.).
  - `hosting_organization` (str): Name of the host institution.
  - `event_level` (str): International/National/State level.
  - `department` (str, optional): Faculty's department.
  - `file` (file, optional): PDF proof of presentation.

## Response Data
- **Code:** `201 Created`
- **Fields:**
  - `id` (UUID): Created record ID.
  - `api_score_faculty` (float): Automatically calculated score.
  - ... (other fields)
