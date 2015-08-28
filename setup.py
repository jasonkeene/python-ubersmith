from setuptools import setup, find_packages


setup(
    name='ubersmith',
    version='0.3.10',
    author='Jason Keene',
    author_email='jasonkeene@gmail.com',
    description='Client library for the Ubersmith API 2.0',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests']),
    install_requires=open('requirements.txt').read().strip().split('\n'),
    url='https://github.com/jasonkeene/python-ubersmith',
    license='MIT License',
    keywords=['ubersmith'],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
