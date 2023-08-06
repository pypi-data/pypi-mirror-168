from setuptools import setup, find_packages

__version__ = '1.0.11' # 版本号
requirements = open('requirements.txt').readlines() # 依赖文件
setup(
    name='rerank_feature_generator', # 在pip中显示的项目名称
    version=__version__,
    author='huyi',
    author_email='huyi@datagrand.com',
    url='https://pypi.org/project/rerank_feature_generator',
    description='version',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6.0',
    install_requires=requirements # 安装依赖
)