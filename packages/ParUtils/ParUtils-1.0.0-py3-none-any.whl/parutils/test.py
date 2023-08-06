from .string import like
from .logging import log


def ttry(f, e_ref, *args, **kwargs):

    exception_occured = False
    try:
        f(*args, **kwargs)
    except Exception as e:
        assert like(str(e), e_ref)
        log(f"[ttry] Exception caught match expected ('{e_ref}')")
        exception_occured = True

    assert exception_occured
