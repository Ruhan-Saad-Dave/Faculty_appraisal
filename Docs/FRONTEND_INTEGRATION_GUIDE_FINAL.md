# Faculty Appraisal System - Exhaustive API Integration Guide (V1)

This document provides the exact field requirements and methods for every backend endpoint.

## Global Information
- **Base URL:** `https://your-cloud-run-url.a.run.app`
- **Auth:** `Authorization: Bearer <SUPABASE_JWT>`
- **Content-Types:**
    - Routes with `file` upload: `multipart/form-data`
    - Summary/Remarks routes: `application/json`

---

## 3. Part B - Research & Professional Development
*Prefix: `/api/v1/part-b`*

### 3.1 Journal Publications
- **POST** `/journal-publications` (Form-Data)
    - **Fields:**
        - `sr_no` (int, optional).
        - `title_with_page_nos` (str, optional).
        - `journal_details` (str, optional).
        - `issn_isbn_no` (str, optional).
        - `indexing` (Enum: `SCOPUS`, `WOS`, `UGC_CARE`, `PEER_REVIEWED`).
        - `department` (str, optional).
        - `file` (file, optional): PDF proof.
    - **Response:** `JournalPublicationResponse`.

- **GET** `/journal-publications/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `JournalPublicationResponse`.

- **GET** `/journal-publications`
    - **Access:** Admin, Dean, VC.
    - **Response:** List of `JournalPublicationResponse`.

- **PUT** `/journal-publications/{publication_id}` (JSON)
    - **Update Logic:**
        - Faculty can update base fields.
        - HOD can update `api_score_hod`.
        - Director can update `api_score_director`.
    - **Response:** `JournalPublicationResponse`.

- **DELETE** `/journal-publications/{publication_id}`
    - **Access:** Owner or higher authority.
    - **Response:** 204 No Content.

- **GET** `/journal-publications/summary/{faculty_id}`
    - **Response:** `{"total_score": float}` (Max 120).

### 3.2 Book Publications
- **POST** `/book-publications` (Form-Data)
    - **Fields:**
        - `title_and_pages` (str, required).
        - `book_title_editor` (str, required).
        - `issn_isbn` (str, required).
        - `publisher_type` (str, required).
        - `co_authors_count` (int, required).
        - `is_first_author` (bool, optional): Default `False`.
        - `department` (str, optional).
        - `file` (file, optional): PDF proof.
    - **Response:** `BookPublicationResponse`.

- **GET** `/book-publications/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `BookPublicationResponse`.

- **GET** `/book-publications`
    - **Access:** Admin only.
    - **Response:** List of `BookPublicationResponse`.

- **PUT** `/book-publications/{publication_id}` (JSON)
    - **Update Logic:**
        - Faculty can update base fields.
        - HOD/Director/Admin can update scores.
    - **Response:** `BookPublicationResponse`.

- **DELETE** `/book-publications/{publication_id}`
    - **Access:** Owner or higher authority.
    - **Response:** 204 No Content.

- **GET** `/book-publications/summary/{faculty_id}`
    - **Response:** `{"total_score": float}`.

### 3.3 Conference Papers
- **POST** `/conferences` (Form-Data)
    - **Fields:**
        - `event_title` (str, required).
        - `event_date` (date, required): YYYY-MM-DD.
        - `activity_type` (str, required): e.g. "Lecture", "Paper Presentation".
        - `hosting_organization` (str, required).
        - `event_level` (str, required): e.g. "International", "National".
        - `department` (str, optional).
        - `file` (file, optional): PDF proof.
    - **Response:** `ConferencePaperResponse`.

- **GET** `/conferences/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `ConferencePaperResponse`.

- **GET** `/conferences`
    - **Access:** Admin only.
    - **Response:** List of `ConferencePaperResponse`.

- **PUT** `/conferences/{paper_id}` (JSON)
    - **Update Logic:**
        - Faculty can update base fields.
        - HOD/Director/Admin can update scores.
    - **Response:** `ConferencePaperResponse`.

- **DELETE** `/conferences/{paper_id}`
    - **Access:** Owner or higher authority.
    - **Response:** 204 No Content.

- **GET** `/conferences/summary/{faculty_id}`
    - **Response:** `{"total_score": float}`.

### 3.4 ICT Pedagogy
- **POST** `/pedagogy` (Form-Data)
    - **Fields:**
        - `title` (str, required).
        - `description` (str, required).
        - `pedagogy_type` (str, required): e.g. "MOOCs", "E-Content".
        - `quadrants` (int, required): 1-4.
        - `department` (str, optional).
        - `file` (file, optional): PDF proof.
    - **Response:** `ICTPedagogyResponse`.

- **GET** `/pedagogy/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `ICTPedagogyResponse`.

- **GET** `/pedagogy`
    - **Access:** Admin only.
    - **Response:** List of `ICTPedagogyResponse`.

- **PUT** `/pedagogy/{pedagogy_id}` (JSON)
    - **Update Logic:**
        - Faculty can update base fields.
        - HOD/Director/Admin can update scores.
    - **Response:** `ICTPedagogyResponse`.

- **DELETE** `/pedagogy/{pedagogy_id}`
    - **Access:** Owner or higher authority.
    - **Response:** 204 No Content.

- **GET** `/pedagogy/summary/{faculty_id}`
    - **Response:** `{"total_score": float}`.

### 3.5 Industrial Training
- **POST** `/industrial-training` (Form-Data)
    - **Fields:**
        - `company_industry` (str, required).
        - `duration_days` (int, required).
        - `nature_of_training` (str, required).
        - `department` (str, optional).
        - `file` (file, optional): PDF proof.
    - **Response:** `IndustrialTrainingResponse`.

- **GET** `/industrial-training/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `IndustrialTrainingResponse`.

- **GET** `/industrial-training`
    - **Access:** Admin only.
    - **Response:** List of `IndustrialTrainingResponse`.

- **PUT** `/industrial-training/{training_id}` (JSON)
    - **Update Logic:**
        - Faculty can update base fields.
        - HOD/Director/Admin can update scores.
    - **Response:** `IndustrialTrainingResponse`.

- **DELETE** `/industrial-training/{training_id}`
    - **Access:** Owner or higher authority.
    - **Response:** 204 No Content.

- **GET** `/industrial-training/summary/{faculty_id}`
    - **Response:** `{"total_score": float}`.

### 3.6 IPR (Patents/Copyrights)
- **POST** `/ipr` (Form-Data)
    - **Fields:**
        - `title` (str, required).
        - `scope` (str, required): e.g. "National", "International".
        - `filing_date` (date, required): YYYY-MM-DD.
        - `status` (str, required): e.g. "Published", "Granted".
        - `patent_file_no` (str, required).
        - `department` (str, optional).
        - `file` (file, optional): PDF proof.
    - **Response:** `IPRResponse`.

- **GET** `/ipr/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `IPRResponse`.

- **GET** `/ipr`
    - **Access:** Admin only.
    - **Response:** List of `IPRResponse`.

- **PUT** `/ipr/{ipr_id}` (JSON)
    - **Update Logic:**
        - Faculty can update base fields.
        - HOD/Director/Admin can update scores.
    - **Response:** `IPRResponse`.

- **DELETE** `/ipr/{ipr_id}`
    - **Access:** Owner or higher authority.
    - **Response:** 204 No Content.

- **GET** `/ipr/summary/{faculty_id}`
    - **Response:** `{"total_score": float}`.

## 1. Part A - Teaching & Contributions
*Prefix: `/api/v1/part-a`*

### 1.1 Teaching Process
- **POST** `/teaching-process` (Form-Data)
    - **Fields:**
        - `sr_no` (int, optional): Serial number.
        - `semester` (str, required): e.g. "Autumn 2025".
        - `course_code_name` (str, required): e.g. "CS101".
        - `planned_classes` (int, required): Target classes.
        - `conducted_classes` (int, required): Actual classes.
        - `department` (str, optional): Faculty department.
        - `file` (file, optional): PDF proof.
    - **Response:** Returns `TeachingProcessResponse` with `id`, `faculty_id`, `api_score_faculty`, `api_score_hod`, and `signature`.

- **GET** `/teaching-process/faculty/{faculty_id}`
    - **Description:** Retrieve all entries for a specific faculty member.
    - **Access:** Owner or higher authority.
    - **Response:** List of `TeachingProcessResponse`.

- **GET** `/teaching-process`
    - **Description:** Retrieve ALL entries in the system.
    - **Access:** Admin only.
    - **Response:** List of `TeachingProcessResponse`.

- **PUT** `/teaching-process/{id}` (JSON)
    - **Description:** Update an existing record.
    - **Access:** Faculty (own), HOD (subordinates), Admin.
    - **Response:** Updated `TeachingProcessResponse`.

- **DELETE** `/teaching-process/{id}`
    - **Description:** Delete a record.
    - **Access:** Admin only.
    - **Response:** 204 No Content.

- **GET** `/teaching-process/summary/{faculty_id}`
    - **Response:** `{"totalMarksOutOf100": float, "scaledMarksOutOf25": float}`.

### 1.2 Course File
- **POST** `/course-files` (Form-Data)
    - **Fields:**
        - `course_paper` (str, required): e.g. "Theory".
        - `title` (str, required): e.g. "Introduction to Algorithms".
        - `sr_no` (int, optional): Serial number.
        - `details_proof` (bool, optional): Default `False`.
        - `department` (str, optional): Faculty department.
        - `file` (file, optional): PDF proof.
    - **Response:** `CourseFileResponse`.

- **GET** `/course-files/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `CourseFileResponse`.

- **GET** `/course-files`
    - **Access:** Admin, Dean, VC.
    - **Response:** List of `CourseFileResponse`.

- **PUT** `/course-files/{id}` (JSON)
    - **Update Logic:** 
        - Faculty can update base fields.
        - HOD/Admin can update `api_score_hod` and `signature`.
    - **Response:** `CourseFileResponse`.

- **DELETE** `/course-files/{id}`
    - **Access:** Owner or higher authority.
    - **Response:** 204 No Content.

- **GET** `/course-files/summary/{faculty_id}`
    - **Response:** `{"totalScore": float}`.

### 1.3 Teaching Methods
- **POST** `/teaching-methods` (Form-Data)
    - **Fields:**
        - `sr_no` (int, optional): Serial number.
        - `short_description` (str, required): e.g. "Use of ICT tools".
        - `details_proof` (bool, optional): Default `False`.
        - `department` (str, optional): Faculty department.
        - `file` (file, optional): PDF proof.
    - **Response:** `TeachingMethodsResponse`.

- **GET** `/teaching-methods/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `TeachingMethodsResponse`.

- **GET** `/teaching-methods`
    - **Access:** Admin only.
    - **Response:** List of `TeachingMethodsResponse`.

- **PUT** `/teaching-methods/{id}` (JSON)
    - **Update Logic:**
        - Faculty can update base fields.
        - HOD/Admin can update scores and signature.
    - **Response:** `TeachingMethodsResponse`.

- **DELETE** `/teaching-methods/{id}`
    - **Access:** Admin only.
    - **Response:** 204 No Content.

- **GET** `/teaching-methods/summary/{faculty_id}`
    - **Response:** `{"totalScore": float}`.

### 1.4 Student Feedback
- **POST** `/student-feedback` (Form-Data)
    - **Fields:**
        - `sr_no` (int, optional): Serial number.
        - `course_code_name` (str, required): e.g. "CS101".
        - `first_feedback` (float, required): 0-5.
        - `second_feedback` (float, required): 0-5.
        - `department` (str, optional): Faculty department.
        - `file` (file, optional): PDF proof.
    - **Response:** `StudentFeedbackResponse`.

- **GET** `/student-feedback/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `StudentFeedbackResponse`.

- **GET** `/student-feedback`
    - **Access:** Admin only.
    - **Response:** List of `StudentFeedbackResponse`.

- **PUT** `/student-feedback/{id}` (JSON)
    - **Update Logic:**
        - Faculty can update base fields.
        - HOD/Director/Admin can update scores.
    - **Response:** `StudentFeedbackResponse`.

- **DELETE** `/student-feedback/{id}`
    - **Access:** Admin only.
    - **Response:** 204 No Content.

- **GET** `/student-feedback/summary/{faculty_id}`
    - **Response:** `{"overallAverage": float}`.

### 1.5 Departmental Activities
- **POST** `/department-activities` (Form-Data)
    - **Fields:**
        - `sr_no` (int, optional): Serial number.
        - `activity` (str, required): e.g. "HOD/Member of Committee".
        - `nature_of_activity` (str, required).
        - `department` (str, optional): Faculty department.
        - `file` (file, optional): PDF proof.
    - **Response:** `DepartmentalActivityResponse`.

- **GET** `/department-activities/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `DepartmentalActivityResponse`.

- **GET** `/department-activities`
    - **Access:** Admin, Dean, VC.
    - **Response:** List of `DepartmentalActivityResponse`.

- **PUT** `/department-activities/{id}` (JSON)
    - **Update Logic:**
        - Faculty can update base fields.
        - HOD/Director/Admin can update scores.
    - **Response:** `DepartmentalActivityResponse`.

- **DELETE** `/department-activities/{id}`
    - **Access:** Owner or higher authority.
    - **Response:** 204 No Content.

- **GET** `/department-activities/summary/{faculty_id}`
    - **Response:** `{"totalScore": float}` (Max 20).

### 1.6 University Activities
- **POST** `/university-activities` (Form-Data)
    - **Fields:**
        - `sr_no` (int, optional): Serial number.
        - `activity` (str, required): e.g. "Senate Member".
        - `nature_of_activity` (str, required).
        - `department` (str, optional): Faculty department.
        - `file` (file, optional): PDF proof.
    - **Response:** `UniversityActivityResponse`.

- **GET** `/university-activities/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `UniversityActivityResponse`.

- **GET** `/university-activities`
    - **Access:** Admin only.
    - **Response:** List of `UniversityActivityResponse`.

- **PUT** `/university-activities/{id}` (JSON)
    - **Update Logic:**
        - Faculty can update base fields.
        - HOD/Director/Admin can update scores.
    - **Response:** `UniversityActivityResponse`.

- **DELETE** `/university-activities/{id}`
    - **Access:** Admin only.
    - **Response:** 204 No Content.

- **GET** `/university-activities/summary/{faculty_id}`
    - **Response:** `{"totalScore": float}` (Max 30).

### 1.7 Social Contributions
- **POST** `/social-contributions` (Form-Data)
    - **Fields:**
        - `sr_no` (int, optional): Serial number.
        - `activity_type` (str, required): e.g. "NSS/NCC".
        - `details_of_activity` (str, required).
        - `department` (str, optional): Faculty department.
        - `file` (file, optional): PDF proof.
    - **Response:** `SocialContributionResponse`.

- **GET** `/social-contributions/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `SocialContributionResponse`.

- **GET** `/social-contributions`
    - **Access:** Admin only.
    - **Response:** List of `SocialContributionResponse`.

- **PUT** `/social-contributions/{id}` (JSON)
    - **Update Logic:**
        - Faculty can update base fields.
        - HOD/Director/Admin can update scores.
    - **Response:** `SocialContributionResponse`.

- **DELETE** `/social-contributions/{id}`
    - **Access:** Admin only.
    - **Response:** 204 No Content.

- **GET** `/social-contributions/summary/{faculty_id}`
    - **Response:** `{"totalScore": float}` (Max 10).

### 1.8 Industry Connect
- **POST** `/industry-connect` (Form-Data)
    - **Fields:**
        - `sr_no` (int, optional): Serial number.
        - `industry_name` (str, required).
        - `details_of_activity` (str, required).
        - `department` (str, optional): Faculty department.
        - `file` (file, optional): PDF proof.
    - **Response:** `IndustryConnectResponse`.

- **GET** `/industry-connect/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `IndustryConnectResponse`.

- **GET** `/industry-connect`
    - **Access:** Admin only.
    - **Response:** List of `IndustryConnectResponse`.

- **PUT** `/industry-connect/{id}` (JSON)
    - **Update Logic:**
        - Faculty can update base fields.
        - HOD/Director/Admin can update scores.
    - **Response:** `IndustryConnectResponse`.

- **DELETE** `/industry-connect/{id}`
    - **Access:** Admin only.
    - **Response:** 204 No Content.

- **GET** `/industry-connect/summary/{faculty_id}`
    - **Response:** `{"totalScore": float}` (Max 5).

### 1.9 Qualification Enhancement
- **POST** `/qualification-enhancement` (Form-Data)
    - **Fields:**
        - `sr_no` (int, optional): Serial number.
        - `qualification_type` (str, required): e.g. "PhD completed".
        - `department` (str, optional): Faculty department.
        - `file` (file, optional): PDF proof.
    - **Response:** `QualificationEnhancementResponse`.

- **GET** `/qualification-enhancement/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `QualificationEnhancementResponse`.

- **GET** `/qualification-enhancement`
    - **Access:** Admin only.
    - **Response:** List of `QualificationEnhancementResponse`.

- **PUT** `/qualification-enhancement/{id}` (JSON)
    - **Update Logic:**
        - Faculty can update base fields.
        - HOD/Director/Admin can update scores.
    - **Response:** `QualificationEnhancementResponse`.

- **DELETE** `/qualification-enhancement/{id}`
    - **Access:** Admin only.
    - **Response:** 204 No Content.

- **GET** `/qualification-enhancement/summary/{faculty_id}`
    - **Response:** `{"totalScore": float}`.

### 1.10 Projects (Part A)
- **POST** `/projects` (Form-Data)
    - **Fields:**
        - `sr_no` (int, optional): Serial number.
        - `project_type` (str, required): e.g. "Major Research Project".
        - `department` (str, optional): Faculty department.
        - `file` (file, optional): PDF proof.
    - **Response:** `ProjectPartAResponse`.

- **GET** `/projects/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `ProjectPartAResponse`.

- **GET** `/projects`
    - **Access:** Admin only.
    - **Response:** List of `ProjectPartAResponse`.

- **PUT** `/projects/{id}` (JSON)
    - **Update Logic:**
        - Faculty can update base fields.
        - HOD/Director/Admin can update scores.
    - **Response:** `ProjectPartAResponse`.

- **DELETE** `/projects/{id}`
    - **Access:** Admin only.
    - **Response:** 204 No Content.

- **GET** `/projects/summary/{faculty_id}`
    - **Response:** `{"totalScore": float}`.

### 1.11 ACR
- **POST** `/acr` (Form-Data)
    - **Access:** Admin only.
    - **Fields:**
        - `faculty_id` (str, required): UUID of the faculty.
        - `subject` (str, required): e.g. "Professional Conduct".
        - `sr_no` (int, optional): Serial number.
        - `department` (str, optional): Faculty department.
        - `file` (file, optional): PDF proof.
    - **Response:** `ACRResponse`.

- **GET** `/acr/faculty/{faculty_id}`
    - **Access:** Owner or higher authority.
    - **Response:** List of `ACRResponse`.

- **GET** `/acr`
    - **Access:** Admin, Dean, VC.
    - **Response:** List of `ACRResponse`.

- **PUT** `/acr/{id}` (JSON)
    - **Update Logic:**
        - HOD/Admin can update `api_score_hod`.
        - Director can update `api_score_director` and `signature`.
    - **Response:** `ACRResponse`.

- **GET** `/acr/summary/{faculty_id}`
    - **Response:** `{"totalScore": float}` (Max 25).

### 1.12 Part A Summary
- **GET** `/part-a-summary/{faculty_id}`
    - **Description:** Aggregates all scores for Part A (Max 200).
    - **Response Structure:**
        ```json
        {
          "teachingScore": 25.0,
          "feedbackScore": 85.0,
          "deptActivityScore": 20.0,
          "universityActivityScore": 30.0,
          "socialScore": 10.0,
          "industryScore": 5.0,
          "acrScore": 25.0,
          "totalFacultyScore": 200.0,
          "totalHodScore": 200.0,
          "totalDirectorScore": 200.0
        }
        ```
