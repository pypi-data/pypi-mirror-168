from setuptools import setup, find_packages
setup(name='Tare',
      version='0.0.1',
      description='Tools of Tare',
      author='QihaoZhu',
      author_email='zhuqh@pku.edu.cn',
      requires= ['numpy','pytorch', 'javalang', 'pickle', 'tqdm'], # 定义依赖哪些模块
      packages=find_packages(),  # 系统自动从当前目录开始找包
      # 如果有的文件不用打包，则只能指定需要打包的文件
      #packages=['代码1','代码2','__init__']  #指定目录中需要打包的py文件，注意不要.py后缀
      license="apache 3.0",
      package_data={'generation':['temp.json']}
      )