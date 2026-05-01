import pytest
from src.setup.dependencies import User

# MOCK DATA FOR HIERARCHY TESTING
SCHOOL_CS_ID = "00000000-0000-0000-0000-000000000001" # Engineering School
SCHOOL_MECH_ID = "00000000-0000-0000-0000-000000000008" # Engineering School (School 8)
SCHOOL_MEDIA_ID = "00000000-0000-0000-0000-000000000004" # Non-Engineering School

FACULTY_ID = "10000000-0000-0000-0000-000000000001"

def test_vc_authority():
    """VC should have authority over anyone across all schools and divisions"""
    vc = User(id="vc_user", roles=["vc"])
    # VC vs Engineering Faculty
    assert vc.has_authority_over(FACULTY_ID, "faculty", subordinate_division="Engineering") is True
    # VC vs Non-Engineering Director
    assert vc.has_authority_over("dir_id", "director", subordinate_division="Non-Engineering") is True

def test_dean_authority():
    """Dean should only have authority over their own division"""
    dean_eng = User(id="dean_eng", roles=["dean"], division="Engineering")
    
    # Authorized: Engineering Faculty
    assert dean_eng.has_authority_over(FACULTY_ID, "faculty", subordinate_division="Engineering") is True
    # Unauthorized: Non-Engineering Faculty (Media School)
    assert dean_eng.has_authority_over("media_fac", "faculty", subordinate_division="Non-Engineering") is False

def test_director_authority():
    """Director should only have authority over their own school"""
    dir_cs = User(id="dir_cs", roles=["director"], school_id=SCHOOL_CS_ID)
    
    # Authorized: Faculty in same school
    assert dir_cs.has_authority_over(FACULTY_ID, "faculty", subordinate_school_id=SCHOOL_CS_ID) is True
    # Unauthorized: Faculty in another Engineering school (School 8)
    assert dir_cs.has_authority_over("mech_fac", "faculty", subordinate_school_id=SCHOOL_MECH_ID) is False

def test_hod_authority_isolation():
    """HOD should have authority only over their own department within their school"""
    hod_cs = User(id="hod_cs", roles=["hod"], school_id=SCHOOL_CS_ID, department="CS")
    
    # Authorized: Faculty in same school AND same department
    assert hod_cs.has_authority_over(FACULTY_ID, "faculty", subordinate_school_id=SCHOOL_CS_ID, subordinate_dept="CS") is True
    
    # Unauthorized: Faculty in same school but DIFFERENT department (ME)
    assert hod_cs.has_authority_over("me_fac", "faculty", subordinate_school_id=SCHOOL_CS_ID, subordinate_dept="ME") is False
    
    # Unauthorized: Faculty in same department (CS) but DIFFERENT school
    assert hod_cs.has_authority_over("other_cs_fac", "faculty", subordinate_school_id=SCHOOL_MECH_ID, subordinate_dept="CS") is False

def test_self_access():
    """Users should always have authority over their own data"""
    faculty = User(id=FACULTY_ID, roles=["faculty"])
    assert faculty.has_authority_over(FACULTY_ID, "faculty") is True

def test_admin_global_access():
    """Admin should have authority over absolutely everything"""
    admin = User(id="admin_user", roles=["admin"])
    assert admin.has_authority_over("any_id", "any_role", subordinate_division="Any", subordinate_school_id="Any") is True

def test_lower_role_cannot_see_higher():
    """Director should NOT have authority over a Dean or VC"""
    director = User(id="dir_id", roles=["director"], school_id=SCHOOL_CS_ID)
    assert director.has_authority_over("dean_id", "dean", subordinate_division="Engineering") is False
    assert director.has_authority_over("vc_id", "vc") is False
