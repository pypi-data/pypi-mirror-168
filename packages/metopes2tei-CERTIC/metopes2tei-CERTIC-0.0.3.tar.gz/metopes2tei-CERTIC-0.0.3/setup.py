import setuptools

setuptools.setup(
    name="metopes2tei-CERTIC",
    version="0.0.3",
    author="Mickaël Desfrênes",
    author_email="mickael.desfrenes@unicaen.fr",
    description="Convert Métopes v3 to TEI",
    long_description="Convert Métopes v3 to TEI",
    long_description_content_type="text/plain",
    url="https://git.unicaen.fr/metopes/metopes-v3-to-tei",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["circe-CERTIC", "argh"],
    python_requires=">=3.9",
    include_package_data=True,
)
