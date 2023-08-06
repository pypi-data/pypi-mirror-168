# from distutils.core import setup
from setuptools import setup, find_packages


setup(
    name = "bsmodule",             # 对外包文件夹的名字
    version = "3.1",               # 版本号
    description = "这是模块测试",    # 描述
    author = "zhang",  # 作者
    author_email = "123@qq.com",  # 作者邮箱
    py_modules = ["module_b6"],  # 模块文件的名字
    # packages = ['beishan','beishan1','beishan.beishan2']  # 指定包
    packages = find_packages()   # 所有包和包内部模块(单独的模块不会发布)
)