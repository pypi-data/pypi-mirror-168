from setuptools import setup, find_packages

str_version = '1.0.6'
readme_file_path = 'README.md'

setup(name='vbigbang_proxy_utils',
      version=str_version,
      description='Commonly used function library by MT',
      url='https://github.com/vbigbang',
      author='vbigbang',
      author_email='i@chenxiaosa.com',
      long_description=open(readme_file_path, encoding='utf-8').read(),
      long_description_content_type='text/markdown',
      license='GPL',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires=['cpca', 'pydantic', 'redis', 'qqwry-py3', 'tenacity', 'requests', 'kafka-python',
                        'vbigbang_thread_logging>=1.0.3'],  # 必要依赖
      python_requires='>=3')
