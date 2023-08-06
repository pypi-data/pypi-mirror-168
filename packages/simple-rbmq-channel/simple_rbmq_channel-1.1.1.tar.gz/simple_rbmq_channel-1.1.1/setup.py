from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='simple_rbmq_channel',
    version='1.1.1',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    url='',
    license='',
    author='anton emelyancev',
    author_email='anttoon@me.com',
    description='Simple rabbitmq tool to publish and receive events synchronously from rabbitmq queues',
    install_requires=[
        'pika==1.3.0',
    ]
)
