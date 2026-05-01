# Update Conference Paper

**Endpoint Name:** Update Conference Paper  
**URL Path:** `/api/v1/part-b/conferences/{paper_id}`  
**Method:** `PUT`

## Description
Updates an existing conference paper record.

## Access Control
- **Faculty:** Update entry fields.
- **HOD/Director:** Update validation scores.

## Request Data
- **Path Parameters:**
  - `paper_id` (UUID string).
- **Body (JSON):**
  - `event_title`, `event_date`, `activity_type`, `hosting_organization`, `event_level`, `research_score_hod`, `research_score_director`.

## Response Data
- **Code:** `200 OK`
