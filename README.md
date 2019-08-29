# Mozilla SSL Configuration Generator, Python edition

This is a command line and Python library version of the
[Mozilla SSL Configuration Generator](https://github.com/mozilla/ssl-config-generator).

Like the original version, this tool builds configuration files to help you
follow the Mozilla
[Server Side TLS](https://wiki.mozilla.org/Security/Server_Side_TLS)
configuration guidelines.

## Why this version ?

The original version provides SSL configuration examples that require to be
manually integrated in the final server software configuration.

The aim of this project is to generate a ready to use configuration that can be
used with automated deployment flows. This may to more easily setup an secure
configuration and keep it up to date with highest security standards.

Generated configurations are fully based on the Mozilla SSL generator, but
with the addition of following extra features:

* Configuration of all paths and variables that needs to be set in original
  templates.
* Inclusion of the user configuration.
* Inclusion of web servers security headers:
    * Addition of recommended security headers.
    * Generation of HTTP Public Key Pinning header from certificate.
    * Configuration helper for some headers like content security policy
      and feature policy. 
