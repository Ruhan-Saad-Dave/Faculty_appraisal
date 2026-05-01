# Delete Research Proposal

**Endpoint Name:** Delete Research Proposal  
**URL Path:** `/api/v1/part-b/research-proposals/{proposal_id}`  
**Method:** `DELETE`

## Description
Deletes a research proposal record.

## Access Control
- **Faculty:** Own records.
- **Admin:** Any record.

## Request Data
- **Path Parameters:**
  - `proposal_id` (UUID string).

## Response Data
- **Code:** `204 No Content`
