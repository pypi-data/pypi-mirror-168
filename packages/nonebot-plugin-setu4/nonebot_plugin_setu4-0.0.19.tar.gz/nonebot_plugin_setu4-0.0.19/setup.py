

from setuptools import find_packages, setup
name = 'nonebot_plugin_setu4'

setup(
    name=name,  
    version='0.0.19',
    author="Special-Week",
    author_email='2385612749@qq.com',
    description="encapsulate logger",
    python_requires=">=3.8.*",
    packages=find_packages(),
    long_description="setu插件",
    url="https://github.com/Special-Week/nonebot_plugin_setu4",

    package_data={name: ['resource/*']},

    # 设置依赖包
    install_requires=["httpx","pillow","nonebot2","nonebot-adapter-onebot"],
)