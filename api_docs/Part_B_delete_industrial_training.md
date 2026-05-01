# Delete Industrial Training

**Endpoint Name:** Delete Industrial Training  
**URL Path:** `/api/v1/part-b/industrial-training/{training_id}`  
**Method:** `DELETE`

## Description
Deletes an industrial training record.

## Access Control
- **Faculty:** Own records.
- **Admin:** Any record.

## Request Data
- **Path Parameters:**
  - `training_id` (UUID string).

## Response Data
- **Code:** `204 No Content`
