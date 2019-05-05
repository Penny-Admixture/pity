import pytest

import bit
from bit.network.services import (
    PeercoinNet,
    NetworkAPI,
    set_service_timeout,
)
from tests.utils import (
    catch_errors_raise_warnings,
    decorate_methods,
    raise_connection_error,
)

from bit.transaction import calc_txid

MAIN_ADDRESS_USED1 = "PT7x6UspGgctp6BPvW7QZksiUWB3yZPEzt"
MAIN_ADDRESS_USED2 = "PLrWFSXP9CkMP7gX3JHgUJgB79rX1n9gMg"
MAIN_ADDRESS_UNUSED = "PM5j5WD1SE3tHQrPe7CKc7wHMQA7fiptiK"
TEST_ADDRESS_USED1 = "n2eMqTT929pb1RDNuqEnxdaLau1rxy3efi"
TEST_ADDRESS_USED2 = "n4Bs2HRTWZfQ9x5Y9KnoU3VJMZq86Lcj7X"
TEST_ADDRESS_UNUSED = "mp1xDKvvZ4yd8h9mLC4P76syUirmxpXhuk"

MAIN_TX_VALID = "41fc12d26d62cbdfe04178ee574ef5ad1e62f5f178dc9fa342d4a2418529e2fe"
TEST_TX_VALID = "d8e42f04d8b31c4ccc5aba022645d8fe4334c3e53dd14972c42b20fcfbc20517"
TX_INVALID = "ff2b4641481f1ee553ba2c9f02f413a86f70240c35b5aee554f84e3efee92210"


def all_items_common(seq):
    initial_set = set(seq[0])
    intersection_lengths = [len(set(s) & initial_set) for s in seq]
    return all_items_equal(intersection_lengths)


def all_items_equal(seq):
    initial_item = seq[0]
    return all(item == initial_item for item in seq if item is not None)


def test_set_service_timeout():
    original = bit.network.services.DEFAULT_TIMEOUT
    set_service_timeout(3)
    updated = bit.network.services.DEFAULT_TIMEOUT

    assert original != updated
    assert updated == 3

    set_service_timeout(original)


class MockBackend(NetworkAPI):
    IGNORED_ERRORS = NetworkAPI.IGNORED_ERRORS
    GET_BALANCE_MAIN = [raise_connection_error]
    GET_TRANSACTIONS_MAIN = [raise_connection_error]
    GET_TRANSACTION_BY_ID_MAIN = [raise_connection_error]
    GET_UNSPENT_MAIN = [raise_connection_error]
    GET_BALANCE_TEST = [raise_connection_error]
    GET_TRANSACTIONS_TEST = [raise_connection_error]
    GET_TRANSACTION_BY_ID_TEST = [raise_connection_error]
    GET_UNSPENT_TEST = [raise_connection_error]


class TestNetworkAPI:
    def test_get_balance_main_equal(self):
        results = [call(MAIN_ADDRESS_USED2) for call in NetworkAPI.GET_BALANCE_MAIN]
        assert all(result == results[0] for result in results)

    def test_get_balance_main_failure(self):
        with pytest.raises(ConnectionError):
            MockBackend.get_balance(MAIN_ADDRESS_USED2)

    def test_get_balance_test_equal(self):
        results = [call(TEST_ADDRESS_USED2) for call in NetworkAPI.GET_BALANCE_TEST]
        assert all(result == results[0] for result in results)

    def test_get_balance_test_failure(self):
        with pytest.raises(ConnectionError):
            MockBackend.get_balance_testnet(TEST_ADDRESS_USED2)

    def test_get_transactions_main_equal(self):
        results = [
            call(MAIN_ADDRESS_USED1)[:100] for call in NetworkAPI.GET_TRANSACTIONS_MAIN
        ]
        assert all_items_common(results)

    def test_get_transactions_main_failure(self):
        with pytest.raises(ConnectionError):
            MockBackend.get_transactions(MAIN_ADDRESS_USED1)

    def test_get_transactions_test_equal(self):
        results = [
            call(TEST_ADDRESS_USED2)[:100] for call in NetworkAPI.GET_TRANSACTIONS_TEST
        ]
        assert all_items_common(results)

    def test_get_transactions_test_failure(self):
        with pytest.raises(ConnectionError):
            MockBackend.get_transactions_testnet(TEST_ADDRESS_USED2)

    def test_get_transaction_by_id_main_equal(self):
        results = [
            calc_txid(call(MAIN_TX_VALID))
            for call in NetworkAPI.GET_TRANSACTION_BY_ID_MAIN
        ]
        assert all_items_equal(results)

    def test_get_transaction_by_id_main_failure(self):
        with pytest.raises(ConnectionError):
            MockBackend.get_transaction_by_id(MAIN_TX_VALID)

    def test_get_transaction_by_id_test_equal(self):
        results = [
            calc_txid(call(TEST_TX_VALID))
            for call in NetworkAPI.GET_TRANSACTION_BY_ID_TEST
        ]
        assert all_items_equal(results)

    def test_get_transaction_by_id_test_failure(self):
        with pytest.raises(ConnectionError):
            MockBackend.get_transaction_by_id_testnet(TEST_TX_VALID)

    def test_get_unspent_main_equal(self):
        results = [call(MAIN_ADDRESS_USED2) for call in NetworkAPI.GET_UNSPENT_MAIN]
        assert all_items_equal(results)

    def test_get_unspent_main_failure(self):
        with pytest.raises(ConnectionError):
            MockBackend.get_unspent(MAIN_ADDRESS_USED1)

    def test_get_unspent_test_equal(self):
        results = [call(TEST_ADDRESS_USED1) for call in NetworkAPI.GET_UNSPENT_TEST]
        assert all_items_equal(results)

    def test_get_unspent_test_failure(self):
        with pytest.raises(ConnectionError):
            MockBackend.get_unspent_testnet(TEST_ADDRESS_USED2)


@decorate_methods(catch_errors_raise_warnings, NetworkAPI.IGNORED_ERRORS)
class TestPeercoinNet:
    def test_get_balance_return_type(self):
        assert isinstance(PeercoinNet.get_balance(MAIN_ADDRESS_USED1), int)

    def test_get_balance_used(self):
        assert PeercoinNet.get_balance(MAIN_ADDRESS_USED1) == 0

    def test_get_balance_unused(self):
        assert PeercoinNet.get_balance(MAIN_ADDRESS_UNUSED) == 0

    def test_get_transactions_return_type(self):
        assert iter(PeercoinNet.get_transactions(MAIN_ADDRESS_USED1))

    def test_get_transactions_used(self):
        assert len(PeercoinNet.get_transactions(MAIN_ADDRESS_USED1)) >= 100

    def test_get_transactions_unused(self):
        assert len(PeercoinNet.get_transactions(MAIN_ADDRESS_UNUSED)) == 0

    def test_get_transaction_by_id_valid(self):
        tx = PeercoinNet.get_transaction_by_id(MAIN_TX_VALID)
        assert calc_txid(tx) == MAIN_TX_VALID

    def test_get_transaction_by_id_invalid(self):
        assert PeercoinNet.get_transaction_by_id(TX_INVALID) == None

    def test_get_unspent_return_type(self):
        assert iter(PeercoinNet.get_unspent(MAIN_ADDRESS_USED1))

    def test_get_unspent_main_used(self):
        assert len(PeercoinNet.get_unspent(MAIN_ADDRESS_USED2)) >= 1

    def test_get_unspent_main_unused(self):
        assert len(PeercoinNet.get_unspent(MAIN_ADDRESS_UNUSED)) == 0
