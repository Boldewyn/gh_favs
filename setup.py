

from distutils.core import setup


setup(
    name = 'gh_favs',
    version = '1.0',
    py_modules = ['gh_favs'],
    author = 'Manuel Strehl',
    author_email = 'boldewyn [at] googlemail.com',
    url = 'http://boldewyn.github.com/gh_favs/',
    description = 'A small script to clone and update all your watched GitHub projects',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Version Control',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Archiving :: Mirroring',
        'Topic :: Utilities',
    ]
)
