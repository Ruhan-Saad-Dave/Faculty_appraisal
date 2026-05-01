# Retrieve Product Developments by Faculty

**Endpoint Name:** Retrieve Product Developments by Faculty  
**URL Path:** `/api/v1/part-b/products/faculty/{faculty_id}`  
**Method:** `GET`

## Description
Retrieves all product development records for a specific faculty member.

## Access Control
- **Higher Authorities:** HOD, Director, Dean, VC.
- **Faculty:** Own records.

## Request Data
- **Path Parameters:**
  - `faculty_id` (UUID string).

## Response Data
- **Code:** `200 OK`
- **Fields (List of Objects):** Standard Product Development fields.
