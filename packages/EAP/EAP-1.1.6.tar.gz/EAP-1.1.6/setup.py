import setuptools

with open("./EAP/Documentation.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "EAP", # package name
    version = "1.1.6", # version
    author = "whyecofiliter", # author name
    author_email = "why_ecofiliter@126.com",
    description = "This package is designed for empirical asset pricing", # description
    long_description = long_description, # documnetation
    long_description_content_type = "text/markdown", # documentation type
    url = "https://github.com/whyecofiliter/EAP", # url in Github
    packages = setuptools.find_packages(), # automatic package searching
    # proto data
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # dependent package
    install_requires = [
        'numpy',
        'pandas',
        'matplotlib',
        'scipy',
        'statsmodels',
        'prettytable',
        'tensorflow',
        'pywavelets',
    ],
    python_requires = '>=3',
    license='MIT'
)