from bit.network.fees import get_fee


def test_get_fee_smol():
    assert get_fee(949) == 0.00949


def test_get_fee_big():
    assert get_fee(3903) == 0.03903
