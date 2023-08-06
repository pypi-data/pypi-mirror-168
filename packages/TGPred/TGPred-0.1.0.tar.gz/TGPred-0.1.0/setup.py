import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='TGPred',
    version='0.1.0',
    author='Ling Zhang',
    author_email='lingzhan@mtu.edu',
    description='TGPred: Efficient methods for predicting target genes of a transcription factor by integrating statistics, machine learning, and optimization.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url='https://github.com/tobefuture/TGPred',
    install_requires=[
        'numpy',
        'pandas',
        'cvxpy',
        'networkx',
        'sklearn'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
