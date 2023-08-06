# from distutils.core import setup
# # from setuptools import setup
#
# # python setup.py sdist
# # python setup.py install
# # python setup.py install --record installed.txt
# setup(
#     name='myai',#需要打包的名字
#     version='v1.0',#版本
#     packages=['tool','base'],
#     py_modules=['tool/utils','base/baseai2','base/baseai5'], # 需要打包的模块
# )
# python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U pip setuptools
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wenutils",
    version="0.0.4",
    author="ai-046",
    author_email="phznai_046@163.com",
    description="wenutils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/zidanewenqsh/wenutils",
    project_urls={
        "Bug Tracker": "https://gitee.com/zidanewenqsh/wenutils",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
