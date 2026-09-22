# Digital Faculty Appraisal System (PBAS)
**Paperless Academic Evaluation & Multi-Tier Review Platform**

---

### 📌 Overview & Context
- **Role:** Backend / Full-Stack Developer
- **Tech Stack:** Python (FastAPI Async), PostgreSQL, SQLAlchemy, React/Vite, Keycloak (OIDC SSO), Docker, GCP (Cloud Run, GCS)
- **Background:** Transitioned the university's annual appraisal process from a legacy, multi-month **paper binder workflow** across 8 schools into a **100% paperless, automated cloud web application**.

---

### 🚀 Key Technical Highlights
- **Async High-Performance Backend:** Engineered non-blocking REST APIs using **FastAPI** & **SQLAlchemy (asyncpg)**, maintaining **<100ms** latency for complex form calculations and queries.
- **Hierarchical Review Engine (RBAC):** Built a strict 5-tier review workflow ($\text{Faculty} \rightarrow \text{HOD} \rightarrow \text{Director} \rightarrow \text{Dean} \rightarrow \text{VC}$) with cross-school division rules and dynamic reviewer scoring.
- **Enterprise Keycloak & Google SSO:** Integrated OIDC Single Sign-On with **DYPIU Keycloak / Google Workspace**, enabling zero-friction login from the central portal and automatic email-to-profile identity linking.
- **Dynamic Form Builder:** Supported multiple appraisal form families (Engineering, Media, Design, Non-Teaching) with real-time score capping, validation, and automated PDF/Excel exports.
- **Cloud & On-Premise Deployment:** Containerized with Docker for multi-worker scaling on **GCP Cloud Run** and local on-premise servers with GCS document storage and SHA-256 deduplication.

---

### 📊 Measurable Impact
- **100% Paperless:** Completely eliminated physical binder submissions, manual paper proofs, and in-person routing.
- **Turnaround Reduction:** Slashed evaluation and score-aggregation cycles from **months to days**.
- **Data Integrity:** Replaced error-prone manual calculations with real-time score aggregation and immutable audit logging.

---

### 📄 Resume Bullet Points (Ready-to-Use)
- *Developed a full-stack, paperless faculty appraisal platform for 8 university schools using FastAPI (Async), PostgreSQL, and React, digitizing a legacy multi-month paper process.*
- *Implemented Keycloak OIDC SSO federated with Google Workspace, featuring automated account linking and a 5-tier hierarchical RBAC review workflow.*
- *Architected high-throughput async database interactions and dynamic form aggregation engines delivering sub-100ms API response times.*
