# Retrieve Industrial Training by Faculty

**Endpoint Name:** Retrieve Industrial Training by Faculty  
**URL Path:** `/api/v1/part-b/industrial-training/faculty/{faculty_id}`  
**Method:** `GET`

## Description
Retrieves all industrial training records for a specific faculty member.

## Access Control
- **Higher Authorities:** HOD, Director, Dean, VC.
- **Faculty:** Own records.

## Request Data
- **Path Parameters:**
  - `faculty_id` (UUID string).

## Response Data
- **Code:** `200 OK`
- **Fields (List of Objects):** Standard Industrial Training fields.
