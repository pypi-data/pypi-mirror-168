import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="prosemble",
    version="0.0.4",
    author="Nana Abeka Otoo",
    author_email="abekaotoo@gmail.com",
    description="Prototype and non prototype-based machine learning package",
    url="https://github.com/naotoo1/prosemble",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=['ensemble', 'Prototype ensemble'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    python_requires='>=3.9',
    py_modules=["prosemble"],
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        'scikit-learn',
        'scipy',
        'matplotlib',

    ]
)
