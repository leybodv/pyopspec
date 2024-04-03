import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


install_requires = [
            "bronkhorst-propar>=1.0,<2.0",
            "pywatlow>=0.1.4",
            "matplotlib>=3.8,<4.0",
    ]

setuptools.setup(
     name='pyopspec',
     version='1.0.0',
     author="Denis Leybo",
     author_email="denis@leybo.xyz",
     description="Program to control operando spectroscopic experiment",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/leybodv/pyopspec",
     packages=setuptools.find_packages(),
     install_requires = install_requires,
     python_requires='>3.10.0',
     entry_points={
                        'console_scripts': [
                                'pyopspec=pyopspec.pyopspec:main',
                        ]},
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
