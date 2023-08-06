import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read().split('----')[0]

setuptools.setup(
    name="qtido",
    version="0.9.6",
    author="Rémi Emonet",
    author_email="remi-242-e2f8@heeere.com",
    description="Tracer de figure et d'animatons, pour l'apprentissage de Python, et plus.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/twitwi/NOT-HERE-qtido/",
    install_requires=['PyQt5'],
    packages=setuptools.find_packages(),
    package_data={
        #'vuejspython.static': ['*.js', '*.css']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
