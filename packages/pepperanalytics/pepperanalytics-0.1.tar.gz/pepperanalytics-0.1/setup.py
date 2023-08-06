from setuptools import setup

setup(name='pepperanalytics', #nombre del paquete en pypi
      version='0.1',  # Development release
      description='Paquete del area Pepper Analytics',
      url='https://github.com/PepperAnalytics/pepperanalytics.git',
      author='Pepper Analytics',
      author_email='raul.marin@peppergroup.es',
      license='MIT',
          packages=['pepperanalytics'], #la carpeta dentro de tu paquete
      zip_safe=False)