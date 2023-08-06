from os.path import abspath, dirname, join
from setuptools import find_packages, setup


ENTRY_POINTS = '''
'''
APP_CLASSIFIERS = [
    'Programming Language :: Python',
    'License :: OSI Approved :: MIT License',
]
APP_REQUIREMENTS = [
    'invisibleroads-macros-process',
]
MARKDOWN_REQUIREMENTS = [
    'markdown',
]
TEST_REQUIREMENTS = [
    'pytest',
    'pytest-cov',
]
FOLDER = dirname(abspath(__file__))
DESCRIPTION = '\n\n'.join(open(join(FOLDER, x)).read().strip() for x in [
    'README.md', 'CHANGES.md'])


setup(
    name='invisibleroads-macros-web',
    version='0.1.0',
    description='Shortcut functions for web operations',
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    classifiers=APP_CLASSIFIERS,
    author='Roy Hyunjin Han',
    author_email='rhh@crosscompute.com',
    url=(
        'https://github.com/invisibleroads/'
        'invisibleroads-macros-web'),
    keywords='invisibleroads',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=APP_REQUIREMENTS,
    extras_require={
        'markdown': MARKDOWN_REQUIREMENTS,
        'test': TEST_REQUIREMENTS,
    },
    entry_points=ENTRY_POINTS)
