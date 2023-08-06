from setuptools import setup, find_packages

#####################################
NAME = "thatool"
VERSION = "1.1.1"
ISRELEASED = True
if ISRELEASED:
    __version__ = VERSION
else:
    __version__ = VERSION + ".dev0"
#####################################


# with open("README.md", "r") as f:
#     long_description = f.read()


setup(
  name = NAME,         # How you named your package folder (MyLib)
  version=__version__,
  description="This package contains several in-house codes to handle some specific tasks. This package is developed and maintained by @thangckt",
  # long_description=long_description,
  author = 'Thang',                         # Type in your name
  author_email = 'thangckt@gmail.com',      # Type in your E-Mail
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  license_files = ('LICENSE.md'),
  url = 'https://github.com/thangckt/thatool',   # Provide either the link to your github or to your website
  download_url="https://github.com/thangckt/thatool/tarball/{}".format(__version__),    # I explain this later on
#   keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best

  packages = find_packages(),
  install_requires=[            # May not use it, due to potential conflict
          # 'scipy', 
          # 'pandas', 
          # 'matplotlib', 
          # 'numpy',
          # 'lmfit', 
          # 'shapely',
          # 'jupyterlab',
      ],

  python_requires='>=3.6',

  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Topic :: Software Development',
    'Programming Language :: Python :: 3.7',
  ],

)



# Ref: https://aaltoscicomp.github.io/python-for-scicomp/packaging/