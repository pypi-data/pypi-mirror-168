import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="proyecto_BRADLEE_KEVIN_JUANPABLO",
    version="1.0.0",
    author="BRADLEE CASTRO-KEVIN ROA-JUAN BELEÑO",
    description="Usamos numpy para desarollar algunos problemas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires= [
        'numpy'
    ]
)