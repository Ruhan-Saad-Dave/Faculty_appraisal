# Update Journal Publication

**Endpoint Name:** Update Journal Publication  
**URL Path:** `/api/v1/part-b/journal-publications/{publication_id}`  
**Method:** `PUT`

## Description
Updates an existing journal publication record. The allowed updates depend on the role of the user.

## Access Control
- **Faculty:** Can update their own submission fields (title, journal, etc.).
- **HOD:** Can ONLY update `api_score_hod`.
- **Director:** Can ONLY update `api_score_director`.

## Request Data
- **Path Parameters:**
  - `publication_id` (UUID string): The unique identifier of the publication record.
- **Body (JSON):**
  - **Faculty Fields:** `sr_no`, `title_with_page_nos`, `journal_details`, `issn_isbn_no`, `indexing`, `department`.
  - **HOD Fields:** `api_score_hod`.
  - **Director Fields:** `api_score_director`.

## Response Data
- **Code:** `200 OK`
- **Fields:** Updated Journal Publication object.
