# Retrieve Self-Development FDP by Faculty

**Endpoint Name:** Retrieve Self-Development FDP by Faculty  
**URL Path:** `/api/v1/part-b/self-development/faculty/{faculty_id}`  
**Method:** `GET`

## Description
Retrieves all FDP participation records for a specific faculty member.

## Access Control
- **Higher Authorities:** HOD, Director, Dean, VC.
- **Faculty:** Own records.

## Request Data
- **Path Parameters:**
  - `faculty_id` (UUID string).

## Response Data
- **Code:** `200 OK`
- **Fields (List of Objects):** Standard Self-Development FDP fields.
