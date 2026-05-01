# Retrieve All Book Publications

**Endpoint Name:** Retrieve All Book Publications  
**URL Path:** `/api/v1/part-b/book-publications`  
**Method:** `GET`

## Description
Retrieves all book publication records across the institution.

## Access Control
- **Authorized Roles:** Admin, Dean, VC.

## Request Data
- **Query Parameters:**
  - `skip` (int, optional): Number of records to skip.
  - `limit` (int, optional): Maximum number of records.

## Response Data
- **Code:** `200 OK`
- Standard Book Publication fields.
