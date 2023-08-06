

from setuptools import find_packages, setup
name = 'youth-version-of-setu4'

setup(
    name=name,  
    version='0.0.12',
    author="Special-Week",
    author_email='2385612749@qq.com',
    description="encapsulate logger",
    python_requires=">=3.8.*",
    packages=find_packages(),
    long_description="setu插件",
    url="https://github.com/Special-Week/youth-version-of-setu4",

    package_data={name: ['resource/lolicon.db']},

    # 设置依赖包
    install_requires=["httpx","pillow","nonebot2","nonebot-adapter-onebot"],
)