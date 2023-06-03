import setuptools
from kslab import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kslab", # Replace with your own username
    version=__version__,
    author="Kurokawa",
    author_email="kurokawa.shora.42w@st.kyoto-u.ac.jp",
    description="KS lab tools",
    license="MIT",
    url="",
    install_requires="""

    """
    ,
    entry_points={
        'console_scripts': [
            'corona=corona:main',
        ],
    },
    author="Propella",
    author_email="propella@example.com",
    description="A covoid-19 tracker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
