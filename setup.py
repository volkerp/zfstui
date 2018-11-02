import setuptools




with open('README.md', 'r') as f:
     long_description = '\n' + f.read()


setuptools.setup(
    name = "zfstui",
    version = "0.1.0",
    author = "Volker Poplawski",
    author_email = "volker@openbios.org",
    description = "terminal user interface for the ZFS filesystem",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license = "GPL-3.0",
    url = "http://github.com/volkerp/zfstui",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Console :: Curses",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Filesystems"
    ],
    packages = setuptools.find_packages(),
    scripts = ['bin/zfstui'],
)

