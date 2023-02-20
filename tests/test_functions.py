# test_my_script.py
from src.web_to_gcs import *

def test_fetch_exists():
    try:
        func = getattr(web_to_gcs, fetch)
    except AttributeError:
        func = None
    assert func is not None

def test_clean_exists():
    try:
        func = getattr(web_to_gcs, clean)
    except AttributeError:
        func = None
    assert func is not None

def test_write_local_exists():
    try:
        func = getattr(web_to_gcs, write_local)
    except AttributeError:
        func = None
    assert func is not None
