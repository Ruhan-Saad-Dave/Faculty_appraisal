# Book Publication Score Summary

**Endpoint Name:** Book Publication Score Summary  
**URL Path:** `/api/v1/part-b/book-publications/summary/{faculty_id}`  
**Method:** `GET`

## Description
Retrieves the total API score for all book publications of a faculty member.

## Access Control
- **Higher Authorities:** HOD, Director, Dean, VC.
- **Faculty:** Own summary.

## Request Data
- **Path Parameters:**
  - `faculty_id` (UUID string).

## Response Data
- **Code:** `200 OK`
- **Fields:**
  - `total_score` (float).
