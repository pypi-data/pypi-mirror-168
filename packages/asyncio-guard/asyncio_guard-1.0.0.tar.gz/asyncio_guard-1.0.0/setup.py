from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='asyncio_guard',
    version='1.0.0',
    description='Guard that provide exclusive access to an object',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='python asyncio mutex lock guard',
    author='Dmitry Inyutin',
    author_email='inyutin.da@gmail.com',
    url='https://github.com/inyutin/asyncio_guard',
    license='MIT',
    include_package_data=True,
    packages=find_packages(exclude=["tests", "tests.*"]),
    platforms=['any'],
    python_requires='>=3.7',
    package_data={
        "asyncio_guard": ["py.typed"],
    }
)
