# Get Part A Summary

**URL Path:** `/api/v1/part-a/part-a-summary/{faculty_id}`
**HTTP Method:** `GET`
**Description:** Aggregates scores for all Part A categories.

## Request Data
- **Type:** N/A (Path Parameter)
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| faculty_id | string (UUID) | ID of the faculty member |

## Response Data
- **Success Status Code:** 200 OK
- **Fields:**

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| teachingScore | float | teachingScore |
| feedbackScore | float | feedbackScore |
| deptActivityScore | float | deptActivityScore |
| universityActivityScore | float | universityActivityScore |
| socialScore | float | socialScore |
| industryScore | float | industryScore |
| acrScore | float | acrScore |
| totalFacultyScore | float | totalFacultyScore |
| totalHodScore | float | totalHodScore |
| totalDirectorScore | float | totalDirectorScore |

## Access Control
- **Roles:** Faculty (self), HOD, Director, Dean, VC, Admin.
