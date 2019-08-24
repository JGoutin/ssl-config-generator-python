# coding=utf-8
"""Pytest configuration"""


def pytest_generate_tests(metafunc):
    """
    Generate tests for each server configuration.
    """
    if 'server' in metafunc.fixturenames:
        from ssl_config import SERVERS
        metafunc.parametrize('server', SERVERS, ids=SERVERS)
