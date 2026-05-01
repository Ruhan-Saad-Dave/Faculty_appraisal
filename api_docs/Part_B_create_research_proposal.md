# Create Research Proposal

**Endpoint Name:** Create Research Proposal  
**URL Path:** `/api/v1/part-b/research-proposals`  
**Method:** `POST`

## Description
Adds a new research proposal submitted for funding.

## Access Control
- **Role Required:** `faculty`.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**
  - `proposal_title` (str): Title of the research proposal.
  - `duration` (str): Duration of the project.
  - `funding_agency` (str): Agency to which it's submitted.
  - `grant_amount` (float): Amount of grant requested.
  - `department` (str, optional): Faculty's department.
  - `file` (file, optional): PDF proof of submission.

## Response Data
- **Code:** `201 Created`
- **Fields:** Standard Research Proposal fields.
