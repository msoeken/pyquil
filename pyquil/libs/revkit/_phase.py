from pyquil.quil import Program

from ._utils import _get_temporary_name, _exec_from_file

def phase_oracle(p, qr, function, **kwargs):
    if not isinstance(function, int):
        try:
            import dormouse
            function = dormouse.to_truth_table(function)
        except ModuleNotFoundError:
            raise RuntimeError(
                "The dormouse library needs to be installed in order to "
                "automatically compile Python code into functions.  Try "
                "to install dormouse with 'pip install dormouse'."
            )

    try:
        import revkit
    except ModuleNotFoundError:
        raise RuntimeError(
            "The RevKit Python library needs to be installed and in the "
            "PYTHONPATH in order to call this function")

    revkit.tt(load="0d{}:{}".format(len(qr), function))
    revkit.convert(tt_to_aig = True)
    kwargs.get("synth", revkit.esopps)()
    filename = _get_temporary_name()
    revkit.write_pyquil(filename=filename)
    _exec_from_file(filename, p, qr)

Program.phase_oracle = phase_oracle