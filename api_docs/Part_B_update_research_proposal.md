# Update Research Proposal

**Endpoint Name:** Update Research Proposal  
**URL Path:** `/api/v1/part-b/research-proposals/{proposal_id}`  
**Method:** `PUT`

## Description
Updates an existing research proposal record.

## Access Control
- **Faculty:** Entry fields.
- **HOD/Director:** Validation scores.

## Request Data
- **Path Parameters:**
  - `proposal_id` (UUID string).
- **Body (JSON):**
  - `proposal_title`, `duration`, `funding_agency`, `grant_amount`, `api_score_hod`, `api_score_director`.

## Response Data
- **Code:** `200 OK`
