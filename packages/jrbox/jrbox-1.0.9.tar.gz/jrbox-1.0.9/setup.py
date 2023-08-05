# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
''''''
from setuptools import setup, find_packages

setup(
    name='jrbox',
    version='1.0.9',
    description="tools",
    # long_description=open('./README.MD').read(),
    include_package_data=True,
    author='Jerry[Jirui Zhang]',
    author_email='2226750760@qq.com',
    maintainer='Jerry',
    maintainer_email='2226750760@qq.com',
    license='MIT License',
    url='https://github.com/ruiandxuan/JRtools.git',
    packages=find_packages(),  # 包的目录
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # 设置编写时的python版本
    ],
    python_requires='>=3.7',  # 设置python版本要求
    install_requires=['xlrd==1.2.0',
                      'xlwt',
                      'xlutils',
                      'lxml',
                      'requests-html'
                      ],  # 安装所需要的库
    # entry_points={
    #     'console_scripts': [
    #         ''],
    # },  # 设置命令行工具(可不使用就可以注释掉)
)
