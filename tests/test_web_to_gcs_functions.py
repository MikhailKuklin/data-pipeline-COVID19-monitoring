# Check that required functions are exist in web_to_gcs code

from src.web_to_gcs import fetch, clean, write_local, write_gcs

def test_fetch_exists():
    assert fetch is not None

def test_clean_exists():
    assert clean is not None

def test_write_local_exists():
    assert write_local is not None
    
def test_write_gcs_exists():
    assert write_gcs is not None
