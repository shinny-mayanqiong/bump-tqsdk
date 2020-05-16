# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='tqsdkbump',
    version="1.0.0",
    description='TianQin SDK',
    author='TianQin',
    author_email='mayanqiong@shinnytech.com',
    url='https://www.shinnytech.com/tqsdk',
    python_requires='>=3.6',
    py_modules = ['tqsdkbump'],
    platforms = 'any',
    entry_points = {
        'console_scripts' : [
            # 这一行是安装到命令行运行的关键
            'tqsdkbump=tqsdkbump:main'
        ]
    }
)
# ("EntryPoint must be in 'name=module:attrs [extras]' format", 'tqsdk-bump = tqsdk-bump:main')