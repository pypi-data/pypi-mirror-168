from setuptools import setup, find_packages


setup(
    name='eon_broker_utilities',
    version='0.0.5',
    license='MIT',
    author="Ahmad Salameh",
    author_email='a.salameh@eonaligner.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://bitbucket.org/eon-mes/broker_utilities/src/master',
    keywords='eon broker project',
    install_requires=[
        "pika==1.3.0",
        "requests==2.25.1",
      ],

)