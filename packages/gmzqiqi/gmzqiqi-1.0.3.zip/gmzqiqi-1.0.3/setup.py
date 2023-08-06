
from setuptools import setup
# from distutils.core import setup

def readme_file():
    with open('README.rst','r',encoding='utf-8') as fp:
        return fp.read()


setup(
    name = 'gmzqiqi',
    version ='1.0.3',
    packages=['gmzqi'],
    py_modules=['tools'],
    author='GMZ-426',
    author_email = '1847394932@qq.com',
    description='a function to input this datas',
    url="https://github.com/GMZ-426/Python_code",
    long_description =readme_file()
    # license='MIT'
)
