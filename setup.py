from setuptools import setup, find_packages

setup(
    name="everest-glacier-engine",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["pipeline", "auto_coder_agent", "everest_langgraph_pipeline"],
    install_requires=[
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "pydantic>=2.0.0",
        "openeo>=0.25.0"
    ],
    entry_points={
        "console_scripts": [
            "everest-glacier=pipeline:main",
        ],
    },
)