


import setuptools



with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SWAG_DNN", # Replace with your own username
    version="0.1.25",
    author="Saeid Safaei",
    author_email="saeid.safaei79@gmail.com",
    description="Implimentation of this paper The SWAG Algorithm; a Mathematical Approach that Outperforms Traditional Deep Learning. Theory and Implementation https://arxiv.org/pdf/1811.11813.pdf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
     packages=['SWAG_DNN'],
    install_requires=[            # I get to this in a second

	'keras==2.2.4',
	'Tensorflow==1.13.1'

      ],    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)







