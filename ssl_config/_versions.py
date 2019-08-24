"""
Basic version comparison that try to match semantic versioning as possible.
"""
from re import compile as _compile


class Version:
    """
    Version.

    Args:
        version (str): Version..
        pre (bool): If True, and no prerelease specified, is always
            lower than any other prerelease when comparing.
    """
    # Semantic version regex
    _RE = _compile(
        # Handle proper "major.minor.patch",
        # but also 'major' or 'major.minor' cases
        r'^(?P<major>0|[1-9]\d*)?'
        r'(?P<minor>\.(0|[1-9]\d*))?'
        r'(?P<patch>\.(0|[1-9]\d*))?'
        # Handle properly formatted prereleases and builds
        r'(?P<prerelease>-(0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
        r'(\.(0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*)?'
        r'(?P<build>\+[0-9a-zA-Z-]+(\.[0-9a-zA-Z-]+)*)?'
        # Keep extra trailling non semantic versionning characters.
        r'(?P<trail>.*)?$')

    # Prerelease and build characters filter
    _FILTER = _compile(r'[^a-zA-Z0-9-.]')

    # Prerelease comparison behavior
    _PRE_COMPARE = {
        # Use an empty value to to ensure stable < prerelease
        True: (),
        # Use an ASCII table late character to ensure stable > prerelease
        False: ('~', )}

    def __init__(self, version, pre=False):
        self._version = parts = {
            key: value for key, value in
            self._RE.match(version).groupdict().items() if value}

        # Set if this version should be before or after prereleases
        self._pre = pre

        # Get core version number as integers
        for key in ('major', 'minor', 'patch'):
            parts[key] = int(parts.get(key, '0').lstrip('.'))

        # Remove delimiters
        for key in ('prerelease', 'build'):
            try:
                parts[key] = tuple(parts[key][1:].split('.'))
            except KeyError:
                continue

        # Try to handle trailing characters that does not match semantic version
        # as prerelease or build information to allow comparison
        try:
            prerelease = parts.pop('trail')
        except KeyError:
            pass
        else:
            # Get build information if any
            if 'build' not in parts:
                try:
                    prerelease, build = prerelease.split('+', 1)
                except ValueError:
                    pass
                else:
                    self.build = build

            self.prerelease = '.'.join(parts.get('prerelease', ())) + prerelease

    def __lt__(self, other):
        return self._compare() < other._compare()

    def __le__(self, other):
        return self._compare() <= other._compare()

    def __eq__(self, other):
        return self._compare() == other._compare()

    def __ge__(self, other):
        return self._compare() >= other._compare()

    def __gt__(self, other):
        return self._compare() > other._compare()

    def __ne__(self, other):
        return self._compare() != other._compare()

    def _compare(self):
        """
        Comparable version.

        Returns:
            tuple: Comparable version.
        """
        ver = self._version
        return (ver['major'], ver['minor'], ver['patch'],
                ver.get('prerelease', self._PRE_COMPARE[self._pre]))

    @property
    def major(self):
        """
        Major version

        Returns:
            int: Major version.
        """
        return self._version['major']

    @major.setter
    def major(self, value):
        """
        Major version

        Args:
            value (int): New value.
        """
        self._version['major'] = int(value)

    @property
    def minor(self):
        """
        Minor version

        Returns:
            int: Minor version.
        """
        return self._version['minor']

    @minor.setter
    def minor(self, value):
        """
        Minor version

        Args:
            value (int): New value.
        """
        self._version['minor'] = int(value)

    @property
    def patch(self):
        """
        Patch version

        Returns:
            int: Patch version.
        """
        return self._version['patch']

    @patch.setter
    def patch(self, value):
        """
        Patch version

        Args:
            value (int): New value.
        """
        self._version['patch'] = int(value)

    @property
    def prerelease(self):
        """
        Prerelease version

        Returns:
            str: Prerelease version.
        """
        return '.'.join(self._version.get('prerelease', ()))

    @prerelease.setter
    def prerelease(self, value):
        """
        Prerelease version

        Args:
            value (str): New value.
        """
        self._version['prerelease'] = tuple(
            element.lstrip('0')
            for element in self._FILTER.sub('', value).strip('-.').split('.'))

    @property
    def build(self):
        """
        Build information.

        Returns:
            str: Build version.
        """
        return '.'.join(self._version.get('build', ()))

    @build.setter
    def build(self, value):
        """
        Build information.

        Args:
            value (str): New value.
        """
        self._version['build'] = tuple(self._FILTER.sub(
            '', value).strip('.').split('.'))
