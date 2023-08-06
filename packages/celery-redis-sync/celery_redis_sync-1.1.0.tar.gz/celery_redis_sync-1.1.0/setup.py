from setuptools import setup, find_packages


setup(
    name='celery_redis_sync',
    version='1.1.0',
    author='Zeit Online',
    author_email='zon-backend@zeit.de',
    url='https://github.com/zeitonline/celery_redis_sync',
    description="Synchronous Redis result store backend",
    long_description='\n\n'.join(
        open(x).read() for x in ['README.rst', 'CHANGES.txt']),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='BSD',
    install_requires=[
        'celery',
        'redis',
        'setuptools',
    ],
    extras_require={'test': [
        'pytest',
        'testing.redis',
    ]},
    entry_points={
        'celery.result_backends': [
            'redis = celery_redis_sync.redis_sync:select_backend',
            'rediss = celery_redis_sync.redis_sync:select_backend',
        ],
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
