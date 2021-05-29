import setuptools

setuptools.setup(
    name="geotree",
    version="0.0.2",
    description="GeoTree: nearest-neighbors on geographic coordinates",
    author=u"Kasra Hosseini",
    #author_email="",
    license="MIT License",
    keywords=["KDTree", "Ball tree", "nearest neighbor", "geographic coordinates"],
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    zip_safe = False,
    url="https://github.com/kasra-hosseini/geotree",
    packages = setuptools.find_packages(),
    include_package_data = True,
    platforms="OS Independent",
    python_requires='>=3.6',
    install_requires=["scikit-learn", "scipy", "numpy", "matplotlib"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],

    entry_points={
        'console_scripts': [
            'geotree = geotree.geotree:main',
        ],
    }
)
