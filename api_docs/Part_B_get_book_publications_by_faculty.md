# Retrieve Book Publications by Faculty

**Endpoint Name:** Retrieve Book Publications by Faculty  
**URL Path:** `/api/v1/part-b/book-publications/faculty/{faculty_id}`  
**Method:** `GET`

## Description
Retrieves all book publications (books, chapters, editorships) submitted by a specific faculty member.

## Access Control
- **Higher Authorities:** HOD, Director, Dean, and VC.
- **Faculty:** Can view their own data.

## Request Data
- **Path Parameters:**
  - `faculty_id` (UUID string): The unique identifier of the faculty member.

## Response Data
- **Code:** `200 OK`
- **Fields (List of Objects):**
  - `id` (UUID): Record identifier.
  - `title_and_pages` (str): Title and page numbers.
  - `book_title_editor` (str): Book title and editor details.
  - `issn_isbn` (str): ISSN/ISBN number.
  - `publisher_type` (str): International/National/Local.
  - `co_authors_count` (int): Number of co-authors.
  - `is_first_author` (bool): Whether the faculty is the first/main author.
  - `document` (str): URL to the PDF proof.
  - `api_score_faculty` (float): Score claimed.
  - `api_score_hod` (float): Score by HOD.
  - `api_score_director` (float): Score by Director.
  - `faculty_id` (UUID): ID of the faculty.
