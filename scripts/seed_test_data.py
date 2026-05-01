import sys
import os
from sqlalchemy.orm import Session
import uuid

# Add src to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.setup.database import SessionLocal, engine, Base
from src.models.Part_B.faculty import Faculty
from src.models.Part_A.teaching_process import TeachingProcess
from src.models.Part_B.journal_publication import JournalPublication

def seed_data():
    db = SessionLocal()
    try:
        # 1. Create tables if they don't exist
        print("Ensuring tables are created...")
        Base.metadata.create_all(bind=engine)

        # 2. Check if test faculty exists
        faculty_id = "00000000-0000-0000-0000-000000000001"
        test_faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
        
        if not test_faculty:
            print(f"Creating test faculty with ID: {faculty_id}")
            test_faculty = Faculty(
                id=faculty_id,
                name="Test Faculty User",
                email="test.faculty@university.edu",
                department="Computer Science",
                role="faculty"
            )
            db.add(test_faculty)
            db.commit()
        else:
            print("Test faculty already exists.")

        # 3. Clear existing entries for this faculty to ensure clean state
        print("Cleaning up old test entries...")
        db.query(TeachingProcess).filter(TeachingProcess.faculty_id == faculty_id).delete()
        db.query(JournalPublication).filter(JournalPublication.faculty_id == faculty_id).delete()
        db.commit()

        # 4. Add a sample Teaching Process entry
        print("Seeding sample Part A data...")
        tp = TeachingProcess(
            faculty_id=faculty_id,
            semester="Spring 2026",
            course_code_name="CS101",
            planned_classes=40,
            conducted_classes=40,
            api_score_faculty=50.0, # Full score for demo
            api_score_hod=50.0,
            department="Computer Science"
        )
        db.add(tp)

        # 5. Add a sample Journal Publication entry
        print("Seeding sample Part B data...")
        jp = JournalPublication(
            faculty_id=faculty_id,
            title_with_page_nos="Seeding Test Paper, pp 1-5",
            journal_details="Test Journal Vol 1",
            issn_isbn_no="0000-0000",
            indexing="Scopus",
            api_score_faculty=15.0,
            api_score_hod=15.0,
            department="Computer Science"
        )
        db.add(jp)

        db.commit()
        print("Database seeded successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
