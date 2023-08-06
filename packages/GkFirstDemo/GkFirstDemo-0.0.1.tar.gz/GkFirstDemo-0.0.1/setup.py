from setuptools import setup, find_packages
setup(name='GkFirstDemo',
      version='0.0.1',
      description='gk first demo',
      author='laomaoQAQ',
      author_email='17863923011@163.com',
      requires=[],  # 定义依赖哪些模块
      packages=find_packages(),  # 系统自动从当前目录开始找包
      # packages=['代码1','代码2','__init__'],  #指定目录中需要打包的py文件，注意不要.py后缀
      license="apache 3.0"
      )
