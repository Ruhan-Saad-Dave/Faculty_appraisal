# Update ICT Pedagogy

**Endpoint Name:** Update ICT Pedagogy  
**URL Path:** `/api/v1/part-b/pedagogy/{pedagogy_id}`  
**Method:** `PUT`

## Description
Updates an existing ICT pedagogy record.

## Access Control
- **Faculty:** Entry fields.
- **HOD/Director:** Validation scores.

## Request Data
- **Path Parameters:**
  - `pedagogy_id` (UUID string).
- **Body (JSON):**
  - `title`, `description`, `pedagogy_type`, `quadrants`, `api_score_hod`, `api_score_director`.

## Response Data
- **Code:** `200 OK`
