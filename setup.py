from distutils.core import setup


def get_requirements():
    reqs = open('requirements.txt').read().strip().split('\n')
    for i, r in enumerate(reqs):
        for op in ['<', '>', '==', '<=', '>=', '!=']:
            if op in r:
                reqs[i] = u'{1} ({0}{2})'.format(op, *r.split(op, 1))
    return reqs

setup(
    name='ubersmith',
    version='0.0.1',
    author='Jason Keene',
    author_email='jasonkeene@gmail.com',
    description='Client library for the Ubersmith API 2.0',
    long_description=open('README.rst').read(),
    packages=['ubersmith'],
    requires=get_requirements(),
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
