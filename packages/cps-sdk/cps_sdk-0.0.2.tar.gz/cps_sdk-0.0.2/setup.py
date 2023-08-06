try:
    from setuptools import setup
except:
    from distutils.core import setup
import setuptools

setup(
    name='cps_sdk',
    author='dragons',
    version='0.0.2',
    description='CPS SDK汇总',
    long_description='CPS SDK汇总',
    author_email='521274311@qq.com',
    url='https://gitee.com/kingons/third_sdk',
    packages=setuptools.find_packages(),
    install_requires= [
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
    ],
    zip_safe=True,
)