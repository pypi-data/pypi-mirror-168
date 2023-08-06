from setuptools import setup


install_requires = [
'bidict == 0.22.0',
'biosppy == 1.0.0',
'colorama == 0.4.5',
'colorlog == 6.7.0',
'contourpy == 1.0.5',
'cycler == 0.11.0',
'easydev == 0.12.0',
'fonttools == 4.37.2',
'future == 0.18.2',
'h5py == 3.7.0',
'joblib == 1.2.0',
'kiwisolver == 1.4.4',
'matplotlib == 3.6.0',
'neurokit2 == 0.2.1',
'nolds == 0.5.2',
'numpy == 1.23.3',
'opencv-python == 4.6.0.66',
'packaging == 21.3',
'pandas == 1.4.4',
'pexpect == 4.8.0',
'Pillow == 9.2.0',
'ptyprocess == 0.7.0',
'pyhrv == 0.4.1',
'pyparsing == 3.0.9',
'python-dateutil == 2.8.2',
'pytz == 2022.2.1',
'scikit-learn == 1.1.2',
'scipy == 1.9.1',
'shortuuid == 1.0.9',
'six == 1.16.0',
'sklearn == 0.0',
'spectrum == 0.8.1',
'threadpoolctl == 3.1.0',
'torch == 1.12.1',
'typing_extensions == 4.3.0',
]


setup(
    name ='cmi_biosignal_lib',
    version = '0.0.2',
    description = 'cmilab biosignal library test',
    author = 'cm park',
    author_email = 'jeff4273@yonsei.ac.kr',
    url = None,
    py_modules = ['functions'],
    install_requires=install_requires
)
