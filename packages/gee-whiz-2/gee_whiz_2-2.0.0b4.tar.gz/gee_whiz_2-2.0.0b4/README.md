# Gee Whiz 2

Gee Whiz 2 is a program for managing Guild Wars 2 addons, profiles, and launching the game from a Python program.

[On PyPi](https://pypi.org/project/gee-whiz-2/)
[On Gitea](https://git.jharmison.com/james/gw2)

## Installation

Download the source of a release tag and change into the directory, for example by running the following:

```sh
VERSION=2.0.0-beta4 # Set this to some other tag if you want a specific version
git clone git@git.jharmison.com:james/gw2.git
cd gw2
git checkout $VERSION
```

Once you have a version you want to install in your working directory, you can execute the following to build and install:

```sh
make
sudo make install
```

## Uninstallation

Change into the directory you downloaded the release into originally and run:

```sh
sudo make uninstall
```

## Usage

After installation, there is a file in /etc/gw2/config.yml that may be useful as a starting point for your own configuration. To customize your installation, run the following:

```sh
mkdir -p ~/.config/gw2
cp /etc/gw2/config.yml ~/.config/gw2/
${EDITOR:-nano} ~/.config/gw2/config.yml
```

As Gee Whiz 2 version 2 is still in rapid development, please see `gw2 --help` for more information on command line usage, including management options for other profiles (to save multiple login passwords).
