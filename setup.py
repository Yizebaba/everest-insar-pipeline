from setuptools import setup, find_packages

setup(
    name="everest-glacier-engine",
    version="1.0.1",
    packages=find_packages(),
    py_modules=["pipeline", "auto_coder_agent", "everest_langgraph_pipeline"],
    install_requires=[
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "pydantic>=2.0.0",
        "openeo>=0.25.0",
        "zarr>=2.16.0",
        "fsspec>=2023.6.0",
        "s3fs>=2023.6.0",
        "aiohttp>=3.8.0",
        "numcodecs>=0.11.0",
        "langgraph>=0.2.0",
        "langchain-core>=0.3.0",
    ],
    entry_points={
        "console_scripts": [
            "everest-glacier=pipeline:run_real_pipeline",
        ],
    },
)