#!/usr/bin/env python
"""The setup script."""

from setuptools import setup, find_packages
import pyvisflow as pvf

with open('README.md', encoding='utf8') as readme_file:
    readme = readme_file.read()

requirements = ['bs4', 'pandas']

test_requirements = [
    'pytest>=3',
]

setup(
    author="pyvisflow",
    author_email='568166495@qq.com',
    python_requires='>=3.6',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="...",
    entry_points={
        # 'console_scripts': [
        #     'test_prj=test_prj.cli:main',
        # ],
    },
    install_requires=requirements,
    license="MIT license",
    # long_description=readme,
    include_package_data=True,
    keywords=['visflow', 'vision', 'flow'],
    name='pyvisflow',
    packages=find_packages(include=['pyvisflow', 'pyvisflow.*']),
    data_files=[('template', [
        'pyvisflow/template/index.html',
        'pyvisflow/template/plotly-2.9.0.min.js'
    ])],
    test_suite='__tests',
    tests_require=test_requirements,
    url='https://gitee.com/carson_add/pyvision-next-example',
    version=pvf.__version__,
    zip_safe=False,
)
