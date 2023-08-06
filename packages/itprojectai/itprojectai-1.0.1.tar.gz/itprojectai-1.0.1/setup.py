from distutils.core import setup

with open("README.rst", "r") as f:
    long_description = f.read()

setup(name='itprojectai',  # 包名
      version='1.0.1',  # 版本号
      description='Lib for AI, publish by itproject-manager.com',
      long_description=long_description,
      author='itproject-manager.com',
      author_email='465230373@qq.com',
      url='https://itproject-manager.com',
      install_requires=['numpy', 'scikit-learn'],
      license='BSD License',
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )
