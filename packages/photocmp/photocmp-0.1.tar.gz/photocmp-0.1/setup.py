import setuptools

setuptools.setup(
    name='photocmp',
    version='0.1',
    description='Tool and library to compare sets of images',
    author='Claudio Cusano',
    author_email='claudio.cusano@unipv.it',
    url='https://github.com/claudio-unipv/photocmp',
    packages=setuptools.find_packages(),
    scripts=['bin/photocompare'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy>=1.13.0",
        "Pillow>=5.1.0"
    ],
    python_requires='>=3.6',
)


# python3 setup.py sdist bdist_wheel
# pip install dist/photocmp-x.x.tar.gz
# python3 -m twine upload dist/*
