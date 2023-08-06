import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ironegg",
    version="1.0.8",
    author="xingyang",
    author_email="xing.yang@intel.com",
    description="utils strong like ironegg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yxzoro/ironegg",
    license='MIT License',
    packages=setuptools.find_packages(),
    install_requires=['django', 'sqlalchemy'],
    classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries'
      ],
)

# make pip package and upload to pypi:
#   python setup.py sdist build
#   twine upload dist/* 
