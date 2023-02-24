# Check that required functions are exist in web_to_gcs code

from src.gcs_to_bq import *

def test_extract_from_gcs_exists():
    assert extract_from_gcs is not None

def test_fetch_exists():
    assert fetch is not None

def test_write_bq_exists():
    assert write_bq is not None
    
def test_gcs_to_bq_exists():
    assert gcs_to_bq is not None
