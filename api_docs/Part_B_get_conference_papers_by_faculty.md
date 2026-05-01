# Retrieve Conference Papers by Faculty

**Endpoint Name:** Retrieve Conference Papers by Faculty  
**URL Path:** `/api/v1/part-b/conferences/faculty/{faculty_id}`  
**Method:** `GET`

## Description
Retrieves all conference papers submitted by a specific faculty member.

## Access Control
- **Higher Authorities:** HOD, Director, Dean, and VC.
- **Faculty:** Own records.

## Request Data
- **Path Parameters:**
  - `faculty_id` (UUID string).

## Response Data
- **Code:** `200 OK`
- **Fields (List of Objects):** Standard Conference Paper fields.
