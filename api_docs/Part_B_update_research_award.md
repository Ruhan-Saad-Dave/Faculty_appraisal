# Update Research Award

**Endpoint Name:** Update Research Award  
**URL Path:** `/api/v1/part-b/research-awards/{award_id}`  
**Method:** `PUT`

## Description
Updates an existing research award record.

## Access Control
- **Faculty:** Entry fields.
- **HOD/Director:** Validation scores.

## Request Data
- **Path Parameters:**
  - `award_id` (UUID string).
- **Body (JSON):**
  - `award_name`, `award_date`, `awarding_agency`, `level`, `research_score_hod`, `research_score_director`.

## Response Data
- **Code:** `200 OK`
