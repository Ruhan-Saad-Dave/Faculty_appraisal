# Update Self-Development FDP

**Endpoint Name:** Update Self-Development FDP  
**URL Path:** `/api/v1/part-b/self-development/{fdp_id}`  
**Method:** `PUT`

## Description
Updates an existing FDP participation record.

## Access Control
- **Faculty:** Entry fields.
- **HOD/Director:** Validation scores.

## Request Data
- **Path Parameters:**
  - `fdp_id` (UUID string).
- **Body (JSON):**
  - `program_name`, `duration_days`, `organizer`, `api_score_hod`, `api_score_director`.

## Response Data
- **Code:** `200 OK`
