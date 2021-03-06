import pytest
import numpy as np
import itertools

from pyquil.wavefunction import get_bitstring_from_index, Wavefunction, _round_to_next_multiple, _octet_bits


@pytest.fixture()
def wvf():
    return Wavefunction(np.array([1.0, 1.j, 0.000005, 0.02]))


def test_get_bitstring_from_index():
    assert get_bitstring_from_index(0, 2) == '00'
    assert get_bitstring_from_index(3, 3) == '011'

    with pytest.raises(IndexError):
        get_bitstring_from_index(10, 2)


def test_parsers(wvf):
    outcome_probs = wvf.get_outcome_probs()
    assert len(outcome_probs.keys()) == 4

    pp_wvf = wvf.pretty_print()
    # this should round out one outcome
    assert pp_wvf == "(1+0j)|00> + 1j|01> + (0.02+0j)|11>"
    pp_wvf = wvf.pretty_print(1)
    assert pp_wvf == "(1+0j)|00> + 1j|01>"

    pp_probs = wvf.pretty_print_probabilities()
    # this should round out two outcomes
    assert len(pp_probs.keys()) == 2
    pp_probs = wvf.pretty_print_probabilities(5)
    assert len(pp_probs.keys()) == 3


def test_ground_state():
    ground = Wavefunction.zeros(2)
    assert len(ground) == 2
    assert ground.amplitudes[0] == 1.0


def test_rounding():
    for i in range(8):
        if 0 == i % 8:
            assert i == _round_to_next_multiple(i, 8)
        else:
            assert 8 == _round_to_next_multiple(i, 8)
            assert 16 == _round_to_next_multiple(i + 8, 8)
            assert 24 == _round_to_next_multiple(i + 16, 8)


def test_octet_bits():
    assert [0, 0, 0, 0, 0, 0, 0, 0] == _octet_bits(0b0)
    assert [1, 0, 0, 0, 0, 0, 0, 0] == _octet_bits(0b1)
    assert [0, 1, 0, 0, 0, 0, 0, 0] == _octet_bits(0b10)
    assert [1, 0, 1, 0, 0, 0, 0, 0] == _octet_bits(0b101)
    assert [1, 1, 1, 1, 1, 1, 1, 1] == _octet_bits(0b11111111)


def test_probabilities(wvf):
    n_qubits = 2
    bitstrings = [list(x) for x in itertools.product((0, 1), repeat=n_qubits)]
    prob_keys = [''.join(str(b) for b in bs) for bs in bitstrings]
    prob_dict = wvf.get_outcome_probs()
    probs1 = np.array([prob_dict[x] for x in prob_keys])
    probs2 = wvf.probabilities()
    np.testing.assert_array_equal(probs1, probs2)
