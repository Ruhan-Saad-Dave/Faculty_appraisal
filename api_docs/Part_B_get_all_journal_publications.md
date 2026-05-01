# Retrieve All Journal Publications

**Endpoint Name:** Retrieve All Journal Publications  
**URL Path:** `/api/v1/part-b/journal-publications`  
**Method:** `GET`

## Description
Retrieves all journal publication records across the entire institution. Primarily for administrative or university-level oversight.

## Access Control
- **Authorized Roles:** Admin, Dean, VC.

## Request Data
- **Query Parameters:**
  - `skip` (int, optional): Number of records to skip (default: 0).
  - `limit` (int, optional): Maximum number of records to return (default: 100).

## Response Data
- **Code:** `200 OK`
- **Fields (List of Objects):**
  - Standard Journal Publication response fields (see `Retrieve Journal Publications by Faculty`).
