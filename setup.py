import os
from setuptools import setup, find_packages

README_PATH = os.path.join(os.path.abspath(
    os.path.dirname(__file__)),
    'README.rst'
)

dependencies = [
    'Django==1.4.3',
    'django-registration==0.8',
]

setup(
    name='djangolabtests',
    version='0.1',
    description='Testing a reg app using different tools',
    author='Dan Claudiu Pop',
    author_email='danclaudiupop@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=dependencies,
)
