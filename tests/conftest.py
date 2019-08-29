# coding=utf-8
"""Pytest configuration"""
from subprocess import run, PIPE, STDOUT, Popen
from time import sleep

from requests import RequestException
from requests_html import HTMLSession

import pytest

_CACHED = dict(requests_session=HTMLSession())


def get(server, config):
    """
    Get configuration from JS server.

    Args:
        server (str): Server name.
        config (str): Configuration name.

    Returns:
        str: Generated server configuration.
    """
    resp = _CACHED['requests_session'].get(
        'http://localhost:5500/#server=%s&config=%s' % (server, config))
    resp.html.render()
    resp.raise_for_status()
    return str(resp.html.find('#output-config', first=True).full_text)


def pytest_sessionstart(session):
    """
    Initialize reference server.

    Args:
        session (pytest.Session):
    """
    # Initialize a Node.js web server to generate output from Mozilla generator
    run(['npm', 'install'], capture_output=True, check=True,
        cwd='ssl-config-generator', universal_newlines=True)

    # Start server
    _CACHED['web_server'] = Popen(
        ['npm', 'run', 'watch'], stdout=PIPE, stderr=STDOUT,
        cwd='ssl-config-generator', universal_newlines=True)

    # Wait server is ready
    while True:
        try:
            get('apache', 'modern')
        except RequestException:
            if _CACHED['web_server'].poll():
                raise RuntimeError(_CACHED['web_server'].communicate()[0])
            sleep(0.5)
        else:
            break


def pytest_sessionfinish(session):
    """
    Close reference server.

    Args:
        session (pytest.Session):
    """
    _CACHED['web_server'].terminate()


def pytest_generate_tests(metafunc):
    """
    Generate tests for each server configuration.
    """
    if 'server' in metafunc.fixturenames:
        from ssl_config import SERVERS
        metafunc.parametrize('server', SERVERS, ids=SERVERS)


@pytest.fixture(scope="session")
def ref_generate():
    """
    Mozilla reference generator.

    Returns:
        function: Function that generate reference configuration from reference
            Mozilla generator.
    """
    return get
