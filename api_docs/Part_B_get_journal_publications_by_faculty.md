# Retrieve Journal Publications by Faculty

**Endpoint Name:** Retrieve Journal Publications by Faculty  
**URL Path:** `/api/v1/part-b/journal-publications/faculty/{faculty_id}`  
**Method:** `GET`

## Description
Retrieves a list of all journal publications submitted by a specific faculty member.

## Access Control
- **Higher Authorities:** HOD, Director, Dean, and VC can view data of their subordinates.
- **Faculty:** Can view their own data.

## Request Data
- **Path Parameters:**
  - `faculty_id` (UUID string): The unique identifier of the faculty member.
- **Query Parameters:**
  - `skip` (int, optional): Number of records to skip (default: 0).
  - `limit` (int, optional): Maximum number of records to return (default: 100).

## Response Data
- **Code:** `200 OK`
- **Fields (List of Objects):**
  - `id` (UUID): Record identifier.
  - `sr_no` (int): Serial number.
  - `title_with_page_nos` (str): Title of the paper.
  - `journal_details` (str): Journal name and details.
  - `issn_isbn_no` (str): ISSN/ISBN number.
  - `indexing` (string): Indexing type (SCOPUS, WOS, etc.).
  - `department` (str): Department name.
  - `document` (str): URL path to the uploaded PDF proof.
  - `api_score_faculty` (float): Score claimed by faculty.
  - `api_score_hod` (float): Score validated by HOD.
  - `api_score_director` (float): Score validated by Director.
  - `faculty_id` (UUID): ID of the faculty member.
