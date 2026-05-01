# Retrieve Research Proposals by Faculty

**Endpoint Name:** Retrieve Research Proposals by Faculty  
**URL Path:** `/api/v1/part-b/research-proposals/faculty/{faculty_id}`  
**Method:** `GET`

## Description
Retrieves all research proposals for a specific faculty member.

## Access Control
- **Higher Authorities:** HOD, Director, Dean, VC.
- **Faculty:** Own records.

## Request Data
- **Path Parameters:**
  - `faculty_id` (UUID string).

## Response Data
- **Code:** `200 OK`
- **Fields (List of Objects):** Standard Research Proposal fields.
