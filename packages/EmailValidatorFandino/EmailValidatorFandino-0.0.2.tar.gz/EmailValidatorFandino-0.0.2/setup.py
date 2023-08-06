from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='EmailValidatorFandino',
    version='0.0.2',
    description='A validator for email',
    long_description=open('README.txt', encoding="utf8").read() + '\n\n' + open('CHANGELOG.txt', encoding="utf8").read(),
    url='',
    author='Cristian Fandiño',
    author_email='cristian.fandino02@uptc.edu.co',
    license='MIT',
    classifiers=classifiers,
    keywords='email',
    packages=find_packages(),
    install_requires=['']
)