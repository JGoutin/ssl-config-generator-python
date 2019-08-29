#!/usr/bin/env python3
# coding=utf-8
"""Command line entry point"""


def _run_command():
    """
    Command line entry point
    """
    from argparse import ArgumentParser

    # Adds parent directory to sys.path to ensure importing the library properly
    from os.path import dirname, realpath
    import sys
    sys.path.insert(0, dirname(dirname(realpath(__file__))))

    from ssl_config import (
        CONFIGS, SERVERS, GUIDELINES_VERSION, GUIDELINES, generate,
        UnsupportedConfiguration)

    configs = GUIDELINES['configurations']

    # Parser: "accelpy"
    parser = ArgumentParser(
        prog='ssl-config',
        description='SSL config generator (From Mozilla guidelines %s).' %
                    GUIDELINES_VERSION)

    parser.add_argument(
        '--server', '-s', choices=SERVERS,
        help='Server software for witch generate the configuration.')
    parser.add_argument(
        '--config', '-c', choices=CONFIGS, default='intermediate',
        help='Configuration level to generate (Default to "intermediate"). '
             '%s.' % ' ; '.join((
                 "Modern: Services with clients that support TLS 1.3 and don't "
                 "need backward compatibility (Oldest client: %s)" %
                 ', '.join(configs['modern']['oldest_clients']),
                 "Intermediate:  General-purpose servers with a variety of "
                 "clients, recommended for almost all systems (Oldest client: "
                 "%s)" % ', '.join(configs['intermediate']['oldest_clients']),
                 "Old: Compatible with a number of very old clients, and "
                 "should be used only as a last resort  (Oldest client: %s)" %
                 ', '.join(configs['old']['oldest_clients']))))
    parser.add_argument(
        '--output', '-o',
        help="Output file. If not specified, print directly in standard "
             "output.")
    parser.add_argument(
        '--server-version',
        help='Server software version. Latest if not specified')
    parser.add_argument(
        '--openssl-version',
        help='OpenSSL version. Latest if not specified')
    parser.add_argument(
        '--hsts_disable', action='store_true',
        help='Disable HTTP Strict Transport Security.')
    parser.add_argument(
        '--ocsp_disable', action='store_true', help='Disable OCSP stapling.')

    args = parser.parse_args()

    try:
        output = generate(args.server, args.config, args.server_version,
                          args.openssl_version, not args.hsts_disable,
                          not args.ocsp_disable)
        if args.output:
            with open(args.output, 'wt') as out_file:
                out_file.write(output)
        else:
            print(output)

    except UnsupportedConfiguration:
        parser.error(str(UnsupportedConfiguration))
    except KeyboardInterrupt:
        pass
    parser.exit()


if __name__ == '__main__':
    _run_command()
