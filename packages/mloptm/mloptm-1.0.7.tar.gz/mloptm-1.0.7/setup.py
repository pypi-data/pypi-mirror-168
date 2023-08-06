from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_desc = (here / 'README.md').read_text(encoding='utf-8')


setup(
        name='mloptm',
        version='1.0.7',
        description='Implementation of ML Optimization Methods in Python',
        long_description=long_desc,
        long_description_content_type='text/markdown',
        url='https://github.com/moaz-elesawey/mloptm',
        author='Moaz Mohammed El-Essawey',
        author_email='mohammedmiaz3141@gmail.com',
        classifiers=[
            'Development Status :: 5 - Production/Stable',

            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',

            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3 :: Only',
            'License :: OSI Approved :: MIT License',
        ],
        keywords='python, python3, ml, optm, mloptm',
        package_dir={'': 'src'},
        packages=find_packages(where='src'),
        python_requires='>=3.7, <4',
        install_requires=["numpy", "sympy", "matplotlib", "tabulate", "Pillow"],
        project_urls={
        'Source': 'https://github.com/moaz-elesawey/mloptm',
    },
)


