""" 
https://stackoverflow.com/questions/17583443/what-is-the-correct-way-to-share-package-version-with-setup-py-and-the-package
"""

from pkg_resources import get_distribution, DistributionNotFound
import os.path

__all__=["gitlogs"]

try:
    _dist = get_distribution('git-logs')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'gitlogs')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Please install this project with setup.py or visit https://www.github.com/nkilm/git-logs'
else:
    __version__ = _dist.version