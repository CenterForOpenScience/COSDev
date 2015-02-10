.. _osf_setup:

Setting up the OSF
==================


*Work in Progress, please add or edit as necessary.*

This page provides a verbose and detailed instruction to installing OSF. If you are already familiar with Python more compact instructions can be found at the `README <https://github.com/CenterForOpenScience/osf.io>`_ file.

Preparing your development environment for the OSF
**************************************************

Below are quick instructions to get up and running with OSF installation on your local computer. These instructions are prepared for **researchers, technical staff, or developers new to python**.

Virtual Environments
--------------------

Software projects will require different settings for different projects or different versions of libraries installed. If you have a single work environment you will not be able to use two versions of libraries simultaneously. IF you updated a version that is incompatible with other projects in your work environment you will break the code. It's best practice to avoid conflicts as much as possible but since you can't use a different machine for each of your projects it is better to use virtual environments so that instead of a global installation you have individual installations of your programming language that you can then tweak for different reasons. For Python you need to install virtualenv using pip.

Pip is a tool for installing and managing Python packages. Working with libraries in a package format makes it easier to manage and update your applications. Pip is therefore a great tool to install in your system first. PHP has a tool called "Composer" that helps you manage dependencies in a similar way.

Installing pip
--------------

Before you begin, check if Pip is already installed. Open the Terminal application on your Mac (It's under /Applications/Utilities). Type:

    ::

        pip

If you see a long list of options for what to do with pip that means pip is already installed. If pip isn't installed you will get a message that says `command not found`

This time type in your terminal

    ::

        easy_install pip

If you receive a long error that starts with

    ::

        error: can't create or remove files in install directory

this is most likely because you don't have permission to write to a directory and should use **"sudo"**. This might be necessary in the upcoming command line tools as well so if the provided version does not work, add sudo to the front. Try entering

    ::

        sudo easy_install pip

Enter your password to continue installation (See our note about passwords within virtual environments).

Installing Virtualenv
---------------------

Virtualenv is the tool we use to isolate the python environments for each project you need to run. Instaling it is easy. Open Terminal and type

    ::

        pip install virtualenv

We are using pip here to install virtualenv, which is why we needed pip first.

Installing Virtualenvwrapper
----------------------------

Now that you installed virtualenv, why not add an extension that makes it even easier to use virtualenv (Programmers like shortcuts). Virtualenvwrapper does what its name suggests, it wraps the virtual environments so that you can easily manage them and work with multiple environments at once. To install virtualenvwrapper, type this into Terminal

  ::

      pip install virtualenvwrapper

To conclude the installation you need to add the following lines to the end of your bash profile file. If you are using bash this could be .bashrc or .profile. If you are using another like zsh you will need to add this section to the file .zshrc; virtualenvwrapper works with bash, zsh or ksh.

.. note::

   You most likely have bash, and if you don't know what this means, `this article <http://natelandau.com/my-mac-osx-bash_profile/>`_  can explain.

  ::

    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/Devel
    source /usr/local/bin/virtualenvwrapper.sh

The first line shows where the virtual environments are. If you installed virtualenv normally you shouldn't need to adjust this setting. The second line is the folder that has your development projects, this folder should exist before you do anything with virtualenvwrapper. Finally the third file is the location of the virtualenvwrapper.sh file.

.. note::

    If you don't know where a certain file is on your computer you can use the find command in Terminal. To search for virtualenvwrapper.sh file anywhere on your computer type the following:
    ::

        find / -name "virtualenvwrapper.sh"

Once you made the changes remember to load the changed file by typing:

    ::

        source ~/.bash_profile


Creating your virtual environment
---------------------------------

You now have a solid development environment framework you can use for any of your projects. To start using OSF we will create a virtual environment for it.

First lets see which virtual environments you already have by using the command to show the short version of your existing environments.

    ::

        lsvirtualenv -b

You'll see that there isn't anything there yet. Let's create a virtual environment titled "try"

    ::

        mkvirtualenv try

When you make a virtual environment it will automatically enter that environment so to get out of virtual environments type:

    ::

        deactivate

now when you run the lsvirtualenv command above you will see that "try" is listed. To start working on this virtual environment type

    ::

        workon try

Now the terminal lines will change to reflect that you are currently in that environment:

    ::

        (try)$

You can switch environments by typing the name of another existing environment

    ::

        workon another

These commands work from within other environments. To get out of the virtual environment again type:

    ::

        deactivate

To delete a virtual environment type:

   ::

        rmvirtualenv try

Now we can go ahead and create the OSF virtual environment and work on it. This will create and start the virtual environment.

    ::

        mkvirtualenv osf

Next time you need to start osf you will have to type:

    ::

        workon osf

Remember that the reason we created these environments is that next time we need to install something just for OSF we will go to the osf virtual environment we just created. Most the remainder of this page will be within this virtual environment unless otherwise stated.


Installing OSF
**************

Using homebrew
--------------

The next step will be to install TokuMX, but just like we used pip to install virtualenv, we need another cool tool called Homebrew to install TokuMX. Homebrew is a package manager that allows you to install lots of very cool things that are not just python related. You most likely have homebrew. To test this open a new window of terminal and type

    ::

        brew

If you see a list of options you already have homebrew and you can skip this section. If not you will want to install homebrew globally, not just in your osf environment. In your new terminal window paste this command:

    ::

        ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"

Homebrew installation will ask you to press ENTER to continue and enter your password. When it's done installing type

    ::

        brew doctor

This will show any possible errors or other things that need to be done. Homebrew is quite clear about what to do in these cases, usually you need to copy paste the provided commands and run them.

Installing TokuMX
-----------------

TokuMX is a database that OSF uses. It is a fork of MongoDB, which is a widely known and very common database application. If you are coming from PHP you have more likely used MySQL although databases are not programming language specific.

To install TokuMX first refresh your brew install by updating it and then use brew to install TokuMX:

    ::

        brew tap tokutek/tokumx
        brew install tokumx-bin

Installing libxml2 and libxslt
------------------------------

(required for installing lxml; which is a package OSF uses and will later need to be installed)

    ::

        brew install libxml2
        brew install libxslt

Install XCode and Command Line Tools
------------------------------------

You will need the command line tools for development work in Macs. It is a good idea to install XCode. You can find XCode in the App Store for Mac applications.

If XCode is already installed make sure you have the command line tools installed as well:
    - Open Xcode

    - Go to "Preferences"

    - Select "Download" tab

    - Install Command Line Tools

    `Source <http://jaranto.blogspot.com/2012/08/os-x-unable-to-execute-clang-no-such.html>`_

This may now work for some systems. With XCode installed, type on the command line:

    ::

        xcode-select --install

You should get a software update window that will install the command-line tools. If you already have them installed, you'll get an error about not being able to contact the software update server.
`Source <http://stackoverflow.com/questions/19548011/cannot-install-lxml-on-mac-os-x-10-9>`_

Clone or copy the OSF files to local directory
----------------------------------------------

To install the latest files for OSF using SSH, type the following in the folder where you would like osf installed.

    ::

        git clone git@github.com:CenterForOpenScience/osf.io.git


Run OSF installation
--------------------

    ::

        cd osf
        pip install -r dev-requirements.txt

Create your local settings file
-------------------------------

    ::

        cp website/settings/local-dist.py website/settings/local.py

Install node packages with ``npm``
----------------------------------

``npm`` is used to install required Node.JS packages.

.. todo:: In-depth info on npm installation. For now, see the README.

Install front end dependencies with ``bower`` and ``npm``
---------------------------------------------------------

Several front end modules required by OSF are installed using bower. Bower is a front end package manager. To install bower run:

    ::

        npm install -g bower

Within your OSF folder Install dependencies for OSF by running:

    ::

        bower install


Building assets with ``webpack``
--------------------------------

.. todo:: Document webpack installation and usage. For now, see the README.

::

    inv assets -dw


Installing Add on Requirements
------------------------------

OSF uses add ons that provide diverse functionalities. You can decide to work with the add ons or without them. If you don't want add ons you can turn them off. Otherwise you will need to install the add on requirements as well.

During your add on installation some packages will be required and if you don't have them you will receive errors. To avoid errors install the following

**Install xQuartz**

This is required for R installation. The xQuartz installation uses an installer that you can download from the following website:
`https://xquartz.macosforge.org/landing/ <https://xquartz.macosforge.org/landing/>`_

**Install gfortran**

Gfortran will also be required for R installation and can be download as a package installer from this `website <https://gcc.gnu.org/wiki/GFortranBinaries>`_ .

**Install R**

Tap into the location where R installation exists within brew.

    ::

        brew tap homebrew/science

Install R using homebrew

    ::

        brew install R

The following commands will install the requirements for add ons.

    ::

        invoke mfr_requirements
        invoke addon_requirements


Starting up
-----------

Run your TokuMX process:

    ::

        invoke mongo

Note -- TokuMX must be running in order to invoke the server. If the process stops it has failed. Try running  `mongod` for a more informative message. See below for common problems.

Run your local development server:

      ::

          invoke server

You now have both the database and application running. You will see the application address in the terminal window where you entered invoke server. It will most likely be **http://0.0.0.0:5000**. Navigate to this url in your browser to check if it works.

Common Error messages
*********************

**1. Mongodb path /data/db does not exist**

    ::

        sudo mkdir -p /data/db/
        sudo chown `id -u` /data/db

**2. unable to execute clang: No such file or directory**

Xcode Command Line Tools installation is missing or was not successful. Go to the section on installing XCode and follow the steps there.

**3. Unable to lock file: /data/db/mongod.lock**

If the TokuMX server is still running or if you turn off the computer without stopping the server the TokuMX lock file will cause errors. If you see an error like the one below:

    ::

        ...exception in initAndListen: 10310 Unable to lock file: /data/db/mongod.lock. Is a mongod instance already running?, terminating...

first check other terminals to see if TokuMX is running. If it isn't go to the folder  /data/db/mongod.lock and delete the file.

**4. RuntimeError: Broken toolchain: cannot link a simple C program OR clang: error: unknown argument: '-mno-fused-madd'**

Add the following to your bash profile document

    ::

        export CFLAGS=-Qunused-arguments
        export CPPFLAGS=-Qunused-arguments


**5. ImportError: No module named kombu.five**
This error is related to Celery and not part of OSF. Until the source code is improved what you can do is uninstall celery and reinstall using:

    ::

        pip uninstall celery
        pip install celery

**6. Incompatible library version: etree.so requires 12.0.0 or later......**

If you have pip and conda installed, make sure remove lxml from conda and from pip. Then install again using conda.

    ::

        conda remove lxml
        pip uninstall lxml
        conda install lxml

Notes and Tips
--------------

    - Use SSH for git to avoid authentication issues.
    - Don't use SUDO inside virtual environments to install things. Bad things happen.

Sources and Further Reading
***************************

    - PIP Documentation `https://pip.readthedocs.org/en/latest/ <https://pip.readthedocs.org/en/latest/>`_
    - VirtualENV and pip basics `http://www.jontourage.com/2011/02/09/virtualenv-pip-basics/ <http://www.jontourage.com/2011/02/09/virtualenv-pip-basics/>`_
    - VirtualEnv Documentation `http://www.virtualenv.org/en/latest/ <http://www.virtualenv.org/en/latest/>`_
    - VirtualEnv Wrapper `http://virtualenvwrapper.readthedocs.org/en/latest/ <http://virtualenvwrapper.readthedocs.org/en/latest/>`_
    - Homebrew: `http://brew.sh/ <http://brew.sh/>`_
    - Flask `http://flask.pocoo.org <http://flask.pocoo.org>`_
    - mongoDB `https://www.mongodb.org <https://www.mongodb.org>`_
    - TokuMX: `http://www.tokutek.com/tokumx-for-mongodb/ <http://www.tokutek.com/tokumx-for-mongodb/>`_
    - IDE: PyCharm `http://www.jetbrains.com/pycharm/features/ <http://www.jetbrains.com/pycharm/features/>`_
    - How to use your bash profile on Mac: `http://natelandau.com/my-mac-osx-bash_profile/ <http://natelandau.com/my-mac-osx-bash_profile/>`_
