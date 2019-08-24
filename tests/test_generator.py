"""
Test configuration generation
"""


def test_render_template(server):
    """
    Test if error when rendering template.

    Args:
        server (str): Server name.
    """
    # TODO: Comparing output with the JS result ?
    # https://stackoverflow.com/questions/8284765/how-do-i-call-a-javascript-function-from-python

    from ssl_config import generate, CONFIGS, UnsupportedConfiguration

    for config in CONFIGS:
        print('\n%s CONFIGURATION:' % config.upper())
        try:
            generated = generate(server, config)
            assert generate(server, config), config
            print(generated)

        # Some servers does not support TLSv1.3 and should raise proper
        # exception with the modern configuration
        except UnsupportedConfiguration as exception:
            if 'TLSv1.3' in exception.args[0] and config == 'modern':
                print(str(exception))
                continue
            raise
