
from setuptools import setup, find_packages




setup(
    name='Librflxlang',
    version='0.1',
    packages=['librflxlang'],
    package_data={
        'librflxlang':
            ['*.{}'.format(ext) for ext in ('dll', 'so', 'so.*', 'dylib')],
    },
    zip_safe=False,
)
