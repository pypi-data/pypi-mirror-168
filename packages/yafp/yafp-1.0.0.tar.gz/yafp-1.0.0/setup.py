from setuptools import setup

setup(
    name='yafp',
    version='1.0.0',
    license='MIT',
    author="Maxim Teplinsky",
    author_email='email@example.com',
    packages=['yet_another_fastapi_profiler'],
    package_dir={'yet_another_fastapi_profiler': 'yet_another_fastapi_profiler'},
    url='https://github.com/teplinsky-maxim/yet-another-fastapi-profiler',
    keywords='fastapi yet_another_fastapi_profiler filter minimal time',
    install_requires=[
        'fastapi',
    ],
)
