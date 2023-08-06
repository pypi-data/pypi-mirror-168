from setuptools import setup, find_packages

setup(
    name='dwj_tools',
    version='3.0',
    author='丁文杰',
    author_email='359582058@qq.com',
    url='https://github.com/buwu-DWJ/strategy',
    description='私人',
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.h5"],
        "": ["*.xlsx"],
    },
    entry_points={}
)

# 1.先更新版本号
# 2.生成新上传代码
# python setup.py sdist build
# 3.推送
# twine upload dist/*