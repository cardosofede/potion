import setuptools

setuptools.setup(name='potion',
                 version='0.0.1',
                 description='Package for use notion as a ninja',
                 author='Federico Cardoso',
                 author_email='federico.cardoso.e@gmail.com',
                 packages=setuptools.find_packages(),
                 install_requires=[
                     'pandas',
                     'numpy',
                     'requests',
                     'datetime',
                     'ujson',
                     'glom'
                 ])
