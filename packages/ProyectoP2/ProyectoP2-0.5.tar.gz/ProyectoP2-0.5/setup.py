from setuptools import setup

readme = open("./README.md", "r")


setup(
    name='ProyectoP2',
    packages=['ProyectoP2'],  # this must be the same as the name above
    version='0.5',
    description='Esta es la descripcion de mi paquete',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='Juan Quezada',
    author_email='',
    keywords=['testing', 'logging', 'example'],
    classifiers=[ ],
    license='MIT',
    include_package_data=True
)
