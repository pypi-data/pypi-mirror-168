
import setuptools
  
with open("README.md", "r") as fh:
    description = fh.read()
  
setuptools.setup(
    name="nlntest",
    version="1.0.0",
    author="Shapour Mohammadi",
    author_email="shmohmad@ut.ac.ir",
    packages=["nlntest"],
    description="A Package for nonlinearity test of nuivariate and multivariate time series",
    long_description=description,
    long_description_content_type="text/markdown",
    license='MIT',
    python_requires='>=3.10',
    install_requires=['numpy','pandas','pandas_datareader','statsmodels','scipy','sklearn'],
    keywords=['python', 'Linearity Tests','Ramsey Linearity Test',
                  'Keenan Test','Tsay Test','Terasvirta, Lin and Granger Test',
                  'Lee, White and Granger Test'],
)
