from setuptools import setup, find_packages

setup(
    name='magpielib',
    version='1.1.1',
    author='zhongyi',
    author_email='conghoulin@163.com',
    description='magpie struct dependence',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "tornado==6.2",
        "PyYAML==6.0",
        "jsonschema==4.15.0",
        "SQLAlchemy==1.4.40",
        "redis==4.3.4",
        "PyMySQL==1.0.2",
        "alembic==1.8.1",
        "pymysql==1.0.2"
    ],
)
