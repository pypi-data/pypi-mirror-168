from setuptools import setup, find_packages
requirements = ['requests', 'pinatapy-vourhey', 'python_dateutil', 'urllib3']
setup(
    name='MoralisSDK',
    version='1.0.3',
    packages=find_packages(exclude=['tests*']),
    license='GNU General Public License v3.0',
    description='A python wrapper for the Molaris REST API',
    long_description=open('README.md').read(),
    keywords=['MoralisSDK','Moralis package', 'ipfs SDK'],
    install_requires=requirements,
    url='https://github.com/kbm9696/MoralisSDK',
    author='Balamurugan',
    author_email='kbala007.1996@gmail.com',
    long_description_content_type='text/markdown'
)
