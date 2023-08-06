from setuptools import find_packages
from setuptools import setup

with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content if 'git+' not in x]

setup(name='pie_break',
    version="1",
    description="An eye-catching break timer for the screen-bound",
    long_description = "An eye-catching break timer for the screen-bound",
    author="sctrls",
    author_email="donot@email.me",
    url="https://github.com/sctrls/pie_break",
    license="MIT License",
    classifiers=(
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    packages=find_packages(),
    install_requires=requirements,
    test_suite='tests',
    # include_package_data: to install data from MANIFEST.in
    include_package_data=True,
    scripts=['scripts/piebreak'],
    zip_safe=False)
