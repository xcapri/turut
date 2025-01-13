from setuptools import setup, find_packages

setup(
    description='Extract the root domain from a list of domains',
    author='xcapri',
    author_email='N/A',
    url='https://github.com/xcapri/turut',
    name='Turut',                            
    version='0.1',                           
    py_modules=['turut'],                   
    install_requires=[                      
        'tldextract',                       
    ],
    entry_points={                           
        'console_scripts': [
            'turut = turut:main',        
        ],
    },
    packages=find_packages(),             
    include_package_data=True,        
)