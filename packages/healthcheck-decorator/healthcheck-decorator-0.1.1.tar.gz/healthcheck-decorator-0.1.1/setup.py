from setuptools import setup

setup(
    name='healthcheck-decorator',
    packages=['healthcheck_decorator'],
    version='0.1.1',
    keywords=['healtcheck', 'decorator', 'monitoring'],
    description='Decorate a function to monitor if it is executed',
    url='https://github.com/Trafitto/healthcheck-decorator',
    author='Trafitto',
    author_email='develop@trafitto.com',
    install_requires=['redis>=4.3.4',],
    license='MIT',

)
