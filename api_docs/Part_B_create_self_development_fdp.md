# Create Self-Development FDP

**Endpoint Name:** Create Self-Development FDP  
**URL Path:** `/api/v1/part-b/self-development`  
**Method:** `POST`

## Description
Adds a new record for a Faculty Development Program (FDP) attended by the faculty member.

## Access Control
- **Role Required:** `faculty`.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**
  - `program_name` (str): Name of the FDP/STTP/Training.
  - `duration_days` (int): Duration in days.
  - `organizer` (str): Name of the organizing institution.
  - `department` (str, optional): Faculty's department.
  - `file` (file, optional): PDF certificate of participation.

## Response Data
- **Code:** `201 Created`
- **Fields:** Standard Self-Development FDP fields.
