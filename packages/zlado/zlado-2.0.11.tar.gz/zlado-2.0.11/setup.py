# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='zlado',
    version='2.0.11',
    author='桃园路后上天桥',
    author_email='shimuly@qq.com',
    description='ado 显示 ecs列表',
    url='http://www.baidu.com',
    license='MIT',
    packages=find_packages(),  # 包含所有的py文件
    package_data={
        # @see https://www.cnblogs.com/babykick/archive/2012/01/18/2325702.html
        '': ['*.ini']
    },
    python_requires='<3.0',
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
    },
    scripts=[]
)
