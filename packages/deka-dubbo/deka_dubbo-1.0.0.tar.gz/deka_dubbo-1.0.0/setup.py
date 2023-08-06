# coding=utf-8

from setuptools import setup, find_packages
setup(
    name='deka_dubbo',  #
    version='1.0.0',
    description=(
        'pip install deka_dubbo，rabbitmq为中间件的分布式任务框架'
    ),
    author='zy',
    author_email='517826265@qq.com',
    packages=find_packages(),
    include_package_data=True,
    platforms=["all"],
    install_requires=[
        'AMQPStorm==2.7.1',
        'redis2',
        'redis3',
        'redis',
        'deka_plog',
        'pytz'
    ]
)
