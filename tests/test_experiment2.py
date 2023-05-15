"""test portfolio"""
import numpy as np
import pytest
import quantstats as qs

from tinycta.port import build_portfolio


# take two moving averages and apply the sign-function, adjust by volatility
def f(prices, fast=32, slow=96, volatility=32):
    """
    construct cash position
    """
    s = prices.ewm(com=slow, min_periods=100).mean()
    f = prices.ewm(com=fast, min_periods=100).mean()
    std = prices.pct_change().ewm(com=volatility, min_periods=100).std()
    return np.sign(f - s) / std


def test_portfolio(prices):
    """
    test portfolio

    Args:
        prices: adjusted prices of futures
    """
    portfolio = build_portfolio(prices=prices, cashposition=1e6 * f(prices))
    assert qs.stats.sharpe(portfolio.profit) == pytest.approx(0.8712580160989778)
