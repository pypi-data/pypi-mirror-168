import os
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-counter-cache-fuxy',
    version=os.getenv('TRAVIS_TAG', '0.1.3'),
    packages=find_packages(exclude=['tests']),
    license='MIT License',
    description='ddjango-counter-cache-fuxy makes it extremely easy to denormalize and '
                'keep track of related model counts.',
    long_description=open("README.rst", "r").read(),
    long_description_content_type="text/x-rst",
    url='https://github.com/fukszssl247/django-counter-cache-field',
    author='Hat Dao',
    author_email='enjoy3013@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[],
    extras_require={
        'test': [
            'django',
        ]
    },
    test_suite='runtests.runtests',
    tests_require=[
        'django'
    ],
    zip_safe=False,
)
