from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Education',
    'Programming Language :: Python :: 3',
    'Natural Language :: English'
]


setup(
    name='solarbot-upload-image',
    version='0.0.1',
    description='Upload images from robot',
    # long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
    author='Os Madrugas',
    author_email='gabrielmaulyfatec@gmail.com',
    url='',
    license='MIT',
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=['sqlalchemy'],
    keywords='upload images'
)