# To run the FastAPI application:

1.  **Set up your PostgreSQL database:**
    *   Ensure you have a PostgreSQL server running.
    *   Create a database for this application (e.g., `faculty_appraisal_db`).
    *   Create a user with appropriate permissions for this database.

2.  **Configure the database connection:**
    *   Create a file named `.env` in the root directory of the project (`C:\Users\ruhan\Faculty_appraisal`).
    *   Add your database connection string to this `.env` file, following the format in `.env.example`:
        ```
        DATABASE_URL="postgresql://user:password@host:port/database_name"
        ```
        Replace `user`, `password`, `host`, `port`, and `database_name` with your PostgreSQL credentials.

3.  **Run the application:**
    *   Open your terminal in the project root directory (`C:\Users\ruhan\Faculty_appraisal`).
    *   Activate your virtual environment if you are using one (e.g., `.\.venv\Scripts\activate` on Windows).
    *   Run the FastAPI application using Uvicorn:
        ```bash
        uvicorn src.main:app --reload
        ```
    *   The application will start, typically on `http://127.0.0.1:8000`.

4.  **Access the API documentation:**
    *   Once the server is running, you can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.
    *   You can test the "Journal Publications" endpoints from there.

**Important Notes:**
*   The `Base.metadata.create_all(bind=engine)` call in `src/main.py` will automatically create the necessary tables (`faculty` and `journal_publications`) in your database when the application starts for the first time.
*   The authentication (`get_current_user`) is currently mocked. For a production environment, you would replace this with a robust authentication system.
*   The update logic for HOD/Director in `journal_publication.py` is basic. Consider refining it with separate endpoints or more dynamic schema validation for better clarity and control.

Let me know if you'd like me to proceed with implementing the next category or if you have any questions about the current setup.