from pyquil.quil import Program

from ._utils import _get_temporary_name, _exec_from_file

def permutation_oracle(p, qr, permutation, **kwargs):
    try:
        import revkit
    except ModuleNotFoundError:
        raise RuntimeError(
            "The RevKit Python library needs to be installed and in the "
            "PYTHONPATH in order to call this function")

    revkit.read_spec(permutation=" ".join(map(str, permutation)))
    kwargs.get("synth", revkit.tbs)()
    filename = _get_temporary_name()
    revkit.write_pyquil(filename=filename)
    _exec_from_file(filename, p, qr)

Program.permutation_oracle = permutation_oracle