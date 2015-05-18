# -*- coding: utf-8 -*-
import os
import sys
import webbrowser

from invoke import task, run

docs_dir = 'docs'
build_dir = os.path.join(docs_dir, '_build')

@task
def readme(browse=False):
    run('rst2html.py README.rst > README.html')

@task
def clean_docs():
    run("rm -rf %s" % build_dir)

@task
def browse_docs():
    path = os.path.join(build_dir, 'index.html')
    webbrowser.open_new_tab(path)

@task
def docs(clean=False, browse=False):
    if clean:
        clean_docs()
    run("sphinx-build {} {}".format(docs_dir, build_dir), pty=True)
    if browse:
        browse_docs()

@task
def watch(port=8000):
    docs()
    try:
        import sphinx_autobuild
    except ImportError:
        print('ERROR: watch task requires the sphinx_autobuild package.')
        print('Install it with:')
        print('    pip install sphinx-autobuild')
        sys.exit(1)
    run('sphinx-autobuild {} {} --port {}'.format(docs_dir, build_dir, port),
            pty=True, echo=True)

