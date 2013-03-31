import os
from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(
    os.path.dirname(__file__)),
    'README.rst'
)

setup(
    name='djangolabtests',
    version='0.1',
    description='Testing a reg app using different tools',
    author='Testerslab Team',
    author_email='danclaudiupop@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    test_suite="djangolabtests.functional_tests",
)
