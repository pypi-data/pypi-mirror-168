import setuptools
with open('.\lichenggong\\ikun\\version.txt','r') as f1:
    version=f1.readline()
with open("README.md","r",encoding="utf-8") as f:
    long_description=f.read()
setuptools.setup(
    name="lichenggong",
    version=version,
    author="2368916680",
    author_email="2368916680@qq.com",
    description="编程语言：python 3 操作系统：windows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=None,
    include_package_data=True,
    package_data={
        'lichenggong':[
            'ikun/*.*']
        },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    python_requires=">=3"
)
