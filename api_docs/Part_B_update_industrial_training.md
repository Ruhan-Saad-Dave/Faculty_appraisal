# Update Industrial Training

**Endpoint Name:** Update Industrial Training  
**URL Path:** `/api/v1/part-b/industrial-training/{training_id}`  
**Method:** `PUT`

## Description
Updates an existing industrial training record.

## Access Control
- **Faculty:** Entry fields.
- **HOD/Director:** Validation scores.

## Request Data
- **Path Parameters:**
  - `training_id` (UUID string).
- **Body (JSON):**
  - `company_industry`, `duration_days`, `nature_of_training`, `api_score_hod`, `api_score_director`.

## Response Data
- **Code:** `200 OK`
