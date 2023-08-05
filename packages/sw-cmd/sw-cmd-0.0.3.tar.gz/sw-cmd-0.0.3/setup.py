import setuptools

from src.swc import swc

setuptools.setup(
    name="sw-cmd",
    version=swc.__version__,
    include_package_data=True,
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(where="src", include=["*"]),
    python_requires=">=3.8",
    install_requires=[
        "click",
        "art",
    ],
    entry_points="""
        [console_scripts]
        swc=swc.swc:cli
    """,
)
