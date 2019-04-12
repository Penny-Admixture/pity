COST_PER_KBYTE = 0.01
MIN_FEE = 0.001


def set_fee_cache_time(seconds):
    """placeholder to ease the porting"""
    pass


def get_fee(tx_size_bytes: int):
    """Gets the recommended satoshi per byte fee."""

    fee = (tx_size_bytes / 1000) * COST_PER_KBYTE

    if fee <= MIN_FEE:
        return MIN_FEE
    else:
        return round(fee, 5)


def get_fee_cached(tx_size):
    """placeholder to ease the porting"""
    return get_fee(tx_size)
