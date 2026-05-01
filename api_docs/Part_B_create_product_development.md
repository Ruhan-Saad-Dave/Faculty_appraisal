# Create Product Development

**Endpoint Name:** Create Product Development  
**URL Path:** `/api/v1/part-b/products`  
**Method:** `POST`

## Description
Adds a new record for a product developed by the faculty (software, hardware, process, etc.).

## Access Control
- **Role Required:** `faculty`.

## Request Data
- **Type:** `multipart/form-data`
- **Fields:**
  - `product_description` (str): Detailed description of the product.
  - `usage_type` (str): Industrial/Internal usage.
  - `department` (str, optional): Faculty's department.
  - `file` (file, optional): PDF proof/manual/technical document.

## Response Data
- **Code:** `201 Created`
- **Fields:** Standard Product Development fields.
