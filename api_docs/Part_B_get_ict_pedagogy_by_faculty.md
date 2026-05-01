# Retrieve ICT Pedagogy by Faculty

**Endpoint Name:** Retrieve ICT Pedagogy by Faculty  
**URL Path:** `/api/v1/part-b/pedagogy/faculty/{faculty_id}`  
**Method:** `GET`

## Description
Retrieves all ICT-enabled pedagogy resources developed by a specific faculty member.

## Access Control
- **Higher Authorities:** HOD, Director, Dean, VC.
- **Faculty:** Own records.

## Request Data
- **Path Parameters:**
  - `faculty_id` (UUID string).

## Response Data
- **Code:** `200 OK`
- **Fields (List of Objects):**
  - `id`, `title`, `description`, `pedagogy_type`, `quadrants`, `document`, `api_score_faculty`, `api_score_hod`, `api_score_director`, `faculty_id`.
