.. _osf_setup:

Setting up the OSF
==================

*Work in Progress, please add or edit as necessary.*

This page provides detailed instructions for getting up and running with an OSF installation on your local computer.
These instructions are prepared for **researchers, technical staff, or developers new to python**, and primarily focus on Mac OS ( >=10.7).

If you are already familiar with Python, more compact instructions can be found in the OSF `README <https://github.com/CenterForOpenScience/osf.io/blob/develop/README.md>`_ file.

Preparing your development environment for the OSF
**************************************************

Before you can begin to install the OSF, you will first need to install several pre-requisites. You may already have these installed, but instructions are provided to ensure that things are up-to-date.

Installing Homebrew
-------------------

Homebrew is a package manager that allows you to install lots of very cool things that are not just python related. You most likely have homebrew.

Homebrew is a package manager that allows you to install many cool things easily (not just python tools)- it will greatly ease the process of installing OSF requirements. To see if Homebrew is already installed, open a new window in your terminal and type

    ::

        brew

If you see a list of options you already have homebrew and you can skip this section. If not you will want to install homebrew globally, not just in your osf environment. To install it, open a new terminal window and run the following command.

    ::

        ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Or for Linux users::

        ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/linuxbrew/go/install)"


Homebrew installation will ask you to press ENTER to continue and enter your password. When it's done installing type

    ::

        brew doctor

This will show any possible errors or other things that need to be done. Homebrew is quite clear about what to do in these cases; usually you just need to copy paste the provided commands and run them.

Installing Python
-----------------

Now that we have Homebrew, we can install Python.  Python is the programming language that much of the OSF is written in. Even if it is already on your computer, installing the newest version via Homebrew will avoid many common problems for new developers.  It will also automatically install pip, which is a tool to manage Python packages.  To install Python, go to your terminal and run

    ::

        brew install Python


Updating your Path
------------------

Now that you have installed Homebrew, you will need to make a change to help your computer find the newly installed software.
This is done by editing the variable PATH in a file loaded whenever you open a new terminal window.

 The file will usually be in your home directory (such as /Users/your_username, commonly abbreviated as ~). If you are using bash this file could be .bash_profile, .bashrc, or .profile.
 If you are using another terminal like zsh you will need to add this section to the file .zshrc. Further tools installed later like virtualenvwrapper will work with bash, zsh or ksh.

.. note::

   You most likely have bash, and if you don't know what this means, `this article <http://natelandau.com/my-mac-osx-bash_profile/>`_  can explain.

    ::

        open -e ~/.bash_profile

If you get the error "The file .bash_profile does not exist," then run

    ::

        touch ~/.bash_profile
        open -e ~/.bash_profile

In your text editor, add the following line to your .bash_profile

    ::

        PATH=$PATH:/usr/local/bin
And save it.

Finally run

    ::

        source ~/.bash_profile

to load the file.

Installing XCode and Java
-------------------------

You will also need the XCode command line tools and Java to install the OSF.  In the terminal, run

    ::

        xcode-select --install

Followed by

    ::

        brew install Caskroom/cask/java


Virtual Environments
--------------------

A common problem for software developers is how to deal with different projects that all require different settings or library versions.
If your computer had only a single work environment shared by multiple projects, you would not be able to use two versions of libraries simultaneously,
and updating a library for one project could break other things that depend on an older version.

To avoid this problem, Python provides a tool called virtual environments (a.k.a. virtualenvs). Since it is not always possible to avoid conflicts- and not often practical
to use a different computer for each thing you work on- it's best to use Virtual Environments. This lets you have separate, individually customized
Python setups for each thing you are working on.

You can install this tool using ``pip``, which is a tool for installing and managing Python packages. This seems like an extra layer of complexity, but working
with libraries in a package format makes it much easier to manage and update your applications.


Installing Virtualenv
+++++++++++++++++++++

Virtualenv is the tool we use to isolate the python environments for each project you need to run. Installing it is easy. Open Terminal and type

    ::

        pip install virtualenv


Installing Virtualenvwrapper
++++++++++++++++++++++++++++

Now that you installed virtualenv, why not add an extension that makes it even easier to use virtualenv (Programmers like shortcuts). Virtualenvwrapper does what its name suggests, it wraps the virtual environments so that you can easily manage them and work with multiple environments at once. To install virtualenvwrapper, type this into Terminal

    ::

        pip install virtualenvwrapper

To conclude the installation you need to add the following lines to the end of your bash profile file.

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
+++++++++++++++++++++++++++++++++

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


Quick Installing The OSF
************************

After you have installed Homebrew, Python, XCode, Java, virtualenv, and virtualenvwrapper, you are ready to install the OSF.


**1.  Copy the OSF to your machine**

    Navigate to where you want the OSF installed, and run

    ::

        git clone  https://github.com/CenterForOpenScience/osf.io.git


**2.  From the Terminal, enter your virtual environment**

    ::

        workon osf

**3.  Create a local settings file**

    Navigate to the osf.io directory, and run

    ::

        cp website/settings/local-dist.py website/settings/local.py

.. note::
    You may need to clear the WHEELHOUSE environmental variable for setup to function properly.

    ::

      unset WHEELHOUSE

**3.  Install invoke and then use it to start the setup process**

    ::

        pip install invoke
        invoke setup


Installing the OSF one piece at a time
**************************************

Although the automatic installer attempts to be helpful, it may sometimes be necessary to perform the installation steps individually- for example, if you are working on a computer running Linux, or updating an existing installation.
Instructions are provided for Mac OS (using Homebrew), but other operating systems will have their own preferred package management tools.

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


Running The OSF
***************

Quick Start
-----------
To fully run the OSF, the following commands must be run.  Many of these programs will continue to run in order to log output to the console: this is normal!

Therefore, run the following commands each in their own terminal windows, making sure to switch to the OSF virtual environment (and directory) each time:
    ::

            invoke mongo -d  # Runs mongod as a daemon
            invoke mailserver
            invoke rabbitmq
            invoke celery_worker
            invoke elasticsearch
            invoke assets -dw
            invoke server


You now have both the database and application running. You will see the application address in the terminal window where you entered invoke server. It will most likely be **http://localhost:5000/**. Navigate to this url in your browser to check if it works.

To enable log-in, you will also need to run the authentication server.
To do so, consult the fakeCAS `repository <https://github.com/CenterForOpenScience/fakeCAS>`_.
First download the binary file and run the commands specified to run the server.
    
**If you need to develop authentication-related features, there is a process for setting up the full CAS server `here <https://github.com/CenterForOpenScience/docker-library/tree/master/cas>`_.


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

**7.  fatal error: 'libxml/xmlversion.h' file not found #include "libxml/xmlversion.h"**

Problem: Libxml installation fails with the error.

Solution: Xcode Command Line Tools installation is missing or was not successful. Go to the section on installing XCode and follow the steps there.

**8.  high disk watermark [10%] exceeded on ..., shards will be relocated away from this node**

Problem: Mongodb needs 10% of your total disk space to function with the OSF, and more then that to not throw a lot of warnings.

Solution:  Free up space on your disk.



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
