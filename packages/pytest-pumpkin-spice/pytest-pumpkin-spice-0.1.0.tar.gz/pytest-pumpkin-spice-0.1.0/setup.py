import pathlib
import setuptools


def read(*args):
    file_path = pathlib.Path(__file__).parent.joinpath(*args)
    with file_path.open(encoding="utf-8") as f:
        return f.read()


setuptools.setup(
    name="pytest-pumpkin-spice",
    version="0.1.0",
    author="Josh Grant",
    author_email="joshua.m.grant@gmail.com",
    maintainer="Josh Grant",
    maintainer_email="joshua.m.grant@gmail.com",
    license="MIT",
    url="https://github.com/hackebrot/pytest-pumpkin-spice",
    description="A pytest plugin that makes your test reporting pumpkin-spiced",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6",
    install_requires=["pytest>=4.2.1"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["pumpkin_spice = pytest_pumpkin_spice.plugin"]},
    keywords=["pytest", "pumpkin spice", "autumn"],
)
