from setuptools import setup, find_packages

VERSION = '1.0' 
DESCRIPTION = 'Package for nonlinearity test of nuivariate and multivariate time series'
LONG_DESCRIPTION="readme.md"

setup(
       
        name="NonlinTest", 
        version=VERSION,
        author="Shapour Mohammadi",
        author_email="shmohmad@ut.ac.ir",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license = "MIT",
        packages=find_packages(),
        install_requires=['numpy','pandas','statsmodels',
                          'scipy','sklearn','math'], 
        
        keywords=['python', 'Linearity Tests','Ramsey Linearity Test',
                  'Keenan Test','Tsay Test','Terasvirta, Lin and Granger Test',
                  'Lee, White and Granger Test'],
        classifiers= ["Programming Language :: Python :: 3.10",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
