from distutils.core import setup
from setuptools import find_packages

setup(
  name = 'disttf',         
  packages = find_packages(),
  version = '0.1',      
  license='apache-2.0',        
  description = 'Python module providing arbitrary density distribution fit layers for tensorflow',   
  author = 'Simon Klüttermann',                   
  author_email = 'Simon.Kluettermann@cs.tu-dortmund.de',      
  url = 'https://github.com/psorus/disttf',   
  download_url = 'https://github.com/psorus/disttf/archive/v_01.tar.gz',    
  keywords = ['ANOMALY DETECTION', 'OUTLIER DETECTION', 'TENSORFLOW','DENSITY', 'DENSITY FITTING'],   
  install_requires=[            
          'numpy',
          'tensorflow',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Science/Research',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)
