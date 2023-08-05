
import numpy as np
from numpy.distutils.core import setup
from numpy.distutils.misc_util import Configuration


# Create configuration
def configuration(parent_package='', top_path=None):
    config = Configuration('analysis', parent_package, top_path)
    config.add_extension(
        '_analysis_utils',
        sources=['_analysis_utils.pyx'],
        include_dirs=[np.get_include()]
    )
    return config


setup(configuration=configuration)