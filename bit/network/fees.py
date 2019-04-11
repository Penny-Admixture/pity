COST_PER_BYTE = 0.00001


def set_fee_cache_time(seconds):
    """placeholder to ease the porting"""
    pass


def get_fee(tx_size_bytes: int):
    """Gets the recommended satoshi per byte fee."""

    if tx_size_bytes < 1001:
        return 0.01

    else:
        return round(tx_size_bytes * COST_PER_BYTE, 5)


def get_fee_cached(tx_size):
    """placeholder to ease the porting"""
    return get_fee(tx_size)
