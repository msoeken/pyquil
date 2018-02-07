def _get_temporary_name():
    """
    Returns a temporary file name.
    """
    from tempfile import _get_candidate_names, _get_default_tempdir

    return "{}/{}".format(_get_default_tempdir(), next(_get_candidate_names()))


def _exec_from_file(filename, p, qr, remove=True):
    """
    Executes the Python code in 'filename'.
    """
    from pyquil.gates import X, CNOT, CCNOT, SWAP, CSWAP, H, Z, CZ, T

    with open(filename, "r") as f:
        exec(f.read().replace("\0", ""))

    if remove:
        import os
        os.remove(filename)
