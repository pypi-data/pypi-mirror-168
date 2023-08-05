# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='zlado',
    version='3.0.1',
    packages=find_packages(),  # 包含所有的py文件
    package_data={
        # @see https://www.cnblogs.com/babykick/archive/2012/01/18/2325702.html
        '': ['*.ini']
    },
    python_requires='>=3.0',
    # 将数据文件也打包
    include_package_data=True,
    install_requires=[
        'click',
        'aliyun-python-sdk-ecs'
    ],
    entry_points={
        'console_scripts': [
            'ado = zlado.ado:cli',
        ]
    }
)
