"""
Mozilla SSL Generator, Python edition
"""
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

__licence__ = "MPL-2.0"
__copyright__ = "The SSL configurations are copyright Mozilla\n" \
                "The Python library is copyright J.Goutin"

from datetime import date as _date
from json import load as _load, loads as _loads
from os import listdir as _listdir
from os.path import dirname as _dirname, join as _join, splitext as _splitext

from pybars import Compiler as _Compiler
from ssl_config._helpers import HELPERS as _HELPERS
from ssl_config._versions import Version as _Version

_DATA_DIR = _join(_dirname(__file__), '_data')

#: Supported server software
SERVERS = tuple(sorted(
    _splitext(name)[0] for name in _listdir(_join(_DATA_DIR, 'templates'))))

with open(_join(_DATA_DIR, 'guidelines.json'), 'rt') as json_file:
    #: Guidelines information as dict
    GUIDELINES = _load(json_file)

#: Mozilla SSL configuration levels
#:
#: Modern:
#:     Services with clients that support TLS 1.3 and don't need
#:     backward compatibility.
#:
#: Intermediate
#:     General-purpose servers with a variety of clients, recommended for
#:     almost all systems.
#:
#: Old:
#:     Compatible with a number of very old clients, and should be used only as
#:     a last resort.
CONFIGS = tuple(sorted(GUIDELINES['configurations']))

#: Mozilla SSL guidelines version
#: https://wiki.mozilla.org/Security/Server_Side_TLS
GUIDELINES_VERSION = GUIDELINES['version']

#: Python edition major and minor versions match with Mozilla SSL guidelines
#: version.
__version__ = '%s.0-beta.1' % GUIDELINES_VERSION


def _get_configs():
    """
    Get supported pieces of software configurations

    Returns:
        dict: configurations.
    """
    lines = []
    with open(_join(_DATA_DIR, 'configs.js'), 'rt') as file:
        for line in file:
            # Remove comments
            line = line.split('//')[0].strip()

            try:
                key, value = line.split(':', 1)
            except ValueError:
                pass
            else:
                line = '"%s":%s' % (key.strip(), value.strip())

            # Filter lines
            if line and not line.startswith('const '):
                lines.append(line)

    content = ''.join(lines)
    for text, rep_text in (
            # Remove JS variables
            ('noSupportedVersion', 'null'),
            ('module.exports = ', ''),
            # Fix JSON syntax
            (',}', '}'), ("'", '"'), (';', '')):
        content = content.replace(text, rep_text)

    return _loads(content)


def _get_state(server, config='intermediate', server_version=None,
               openssl_version=None, hsts=True, ocsp=True):
    """
    Generates variables used to render configuration templates.

    Args:
        server (str): Server name.
        config (str): Configuration name.
        server_version (str): Server version, latest if not specified.
        openssl_version (str): OpenSSL version, latest if not specified.
        hsts (bool): Enable HTTP Strict Transport Security.
        ocsp (bool): Enable OCSP stapling.

    Returns:
        dict: state
    """
    ssc = GUIDELINES['configurations'][config]

    cfg = _get_configs()
    server_cfg = cfg[server]
    openssl_cfg = cfg['openssl']
    server_name = server_cfg['name']

    server_ver = server_version or server_cfg['latestVersion']
    openssl_ver = openssl_version or openssl_cfg['latestVersion']

    supports_hsts = server_cfg.get('supportsHsts', True)
    supports_ocsp = server_cfg.get('supportsOcspStapling', True)

    # Remove TLS 1.3 if unsupported by software
    protocols = ssc['tls_versions'].copy()
    tls13_ver = server_cfg.get('tls13')
    if (not tls13_ver or
            _Version(server_ver) < _Version(tls13_ver, pre=True) or
            _Version(openssl_ver) < _Version(openssl_cfg['tls13'], pre=True)):
        protocols.remove('TLSv1.3')
        if not protocols:
            raise UnsupportedConfiguration(
                ('%s %s does not support TLSv1.3, '
                 'unable to generate Mozilla "%s" SSL configuration.') % (
                    server_name, server_ver, config))

    # Remove ciphers that are unsupported by software
    ciphers = ssc['ciphers'][server_cfg.get('cipherFormat', 'openssl')]
    supported_ciphers = server_cfg.get('supportedCiphers')
    if supported_ciphers:
        ciphers = [cipher for cipher in ciphers if cipher in supported_ciphers]

    # Select the command to generate the DH parameters files
    dh_param_size = ssc.get('dh_param_size')
    if not dh_param_size:
        dh_command = ''
    elif dh_param_size >= 2048:
        dh_command = 'cat ' + _join(_DATA_DIR, 'ffdhe%d.txt' % dh_param_size)
    else:
        dh_command = 'openssl dhparam %d' % dh_param_size

    return {
        'form': {
            'config': config,
            'hsts': hsts and supports_hsts,
            'ocsp': ocsp and supports_ocsp,
            'opensslVersion': openssl_ver,
            'server': server,
            'serverVersion': server_ver,
            'serverName': server_cfg['name'],
        },
        'output': {
            'ciphers': ciphers,
            'cipherSuites': ssc['ciphersuites'],
            'date': _date.today().isoformat(),
            'dhCommand': dh_command,
            'dhParamSize': dh_param_size,
            'hasVersions': server_cfg.get('hasVersions', True),
            'hstsMaxAge': ssc['hsts_min_age'],
            'latestVersion': server_cfg['latestVersion'],
            'link': ('Mozilla SSL Generator, Python edition %s;'
                     ' %s %s; %s configuration') % (
                __version__, server_name, server_ver, config.capitalize()),
            'oldestClients': ssc['oldest_clients'],
            'opensslCiphers': ciphers,
            'opensslCipherSuites': ssc['ciphersuites'],
            'protocols': protocols,
            'serverPreferredOrder': ssc['server_preferred_order'],
            'showSupports': server_cfg.get('showSupports', True),
            'supportsConfigs': server_cfg.get('supportsConfigs', True),
            'supportsHsts': supports_hsts,
            'supportsOcspStapling': supports_ocsp,
            'usesDhe': any(cipher.startswith('DHE') or
                           '_DHE_' in cipher for cipher in ciphers),
            'usesOpenssl': server_cfg.get('usesOpenssl', True),
        },
        'sstls': GUIDELINES
    }


class UnsupportedConfiguration(Exception):
    """Unsupported Configuration Exception"""


def generate(server, config='intermediate',
             server_version=None, openssl_version=None, hsts=True, ocsp=True):
    """
    Generate configuration.

    Args:
        server (str): Server name.
        config (str): Configuration name.
        server_version (str): Server version, latest if not specified.
        openssl_version (str): OpenSSL version, latest if not specified.
        hsts (bool): Enable HTTP Strict Transport Security.
        ocsp (bool): Enable OCSP stapling.

    Returns:
        str: Configuration file content.
    """
    state = _get_state(
        server, config, server_version, openssl_version, hsts, ocsp)

    with open(_join(_DATA_DIR, 'templates/%s.hbs' % server), 'rt') as hbs_file:
        template = hbs_file.read()

    return _Compiler().compile(template)(state, helpers=_HELPERS)
