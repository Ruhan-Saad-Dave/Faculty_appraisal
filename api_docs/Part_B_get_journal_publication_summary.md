# Journal Publication Score Summary

**Endpoint Name:** Journal Publication Score Summary  
**URL Path:** `/api/v1/part-b/journal-publications/summary/{faculty_id}`  
**Method:** `GET`

## Description
Calculates and retrieves the total aggregated API score for all journal publications for a specific faculty member.

## Access Control
- **Higher Authorities:** HOD, Director, Dean, and VC.
- **Faculty:** Can view their own summary.

## Request Data
- **Path Parameters:**
  - `faculty_id` (UUID string): The unique identifier of the faculty member.

## Response Data
- **Code:** `200 OK`
- **Fields:**
  - `total_score` (float): The sum of validated scores for all journal publications.
