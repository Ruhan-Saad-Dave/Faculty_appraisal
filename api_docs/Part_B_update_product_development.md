# Update Product Development

**Endpoint Name:** Update Product Development  
**URL Path:** `/api/v1/part-b/products/{product_id}`  
**Method:** `PUT`

## Description
Updates an existing product development record.

## Access Control
- **Faculty:** Entry fields.
- **HOD/Director:** Validation scores.

## Request Data
- **Path Parameters:**
  - `product_id` (UUID string).
- **Body (JSON):**
  - `product_description`, `usage_type`, `api_score_hod`, `api_score_director`.

## Response Data
- **Code:** `200 OK`
