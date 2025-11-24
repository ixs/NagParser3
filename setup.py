from distutils.core import setup

VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_PATCH = 31
versionstr = '%s.%s.%s' % (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

# Supporting Python 3.x

setup(
    name='NagParser',
    version=versionstr,
    author='Matt Kennedy & Zeb Palmer',
    author_email='zeb@zebpalmer.com',
    packages=['nagparser', 'nagparser.Client', 'nagparser.Model', 'nagparser.Services', 'nagparser.Tests'],
    #scripts=[ "bin/script.py"]
    url='http://github.com/zebpalmer/NagiosParser',
    license='GPLv3',
    description='Parse realtime Nagios Data from status.dat and objects.cache, do useful stuff with it',
    long_description=open('README.rst').read(),
    classifiers=[
              'Development Status :: 3 - Alpha',
              'Environment :: Console',
              'Environment :: Plugins',
              'Intended Audience :: Developers',
              'Intended Audience :: System Administrators',
              'Intended Audience :: Telecommunications Industry',
              'License :: OSI Approved :: GNU General Public License (GPL)',
              'Natural Language :: English',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.8',
              'Programming Language :: Python :: 3.9',
              'Programming Language :: Python :: 3.10',
              'Programming Language :: Python :: 3.11',
              'Programming Language :: Python :: 3.12',
              'Topic :: Software Development :: Libraries :: Python Modules',
              'Topic :: Utilities'
              ],
)
