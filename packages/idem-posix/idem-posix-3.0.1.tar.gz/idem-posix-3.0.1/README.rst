**********
IDEM-POSIX
**********
**Grains, execution modules, and state modules common to all posix systems**

INSTALLATION
============

Install with pip::

    pip install idem-posix

DEVELOPMENT INSTALLATION
========================


Clone the `idem-posix` repo and install with pip::

    git clone https://gitlab.com/saltstack/pop/idem-posix.git idem_posix
    pip install -e idem_posix

EXECUTION
=========
After installation the `grains` command should now be available

TESTING
=======
install `requirements-test.txt` with pip and run pytest::

    pip install -r idem-posix/requirements-test.txt
    pytest idem-posix/tests

VERTICAL APP-MERGING
====================
Instructions for extending idem-posix into an OS specific pop project

Install pop::

    pip install --upgrade pop

Create a new directory for the project::

    mkdir idem-{specific_posix_os}
    cd idem-{specific_posix_os}


Use `pop-seed` to generate the structure of a project that extends `grains` and `idem`::

    pop-seed -t v idem-{specific_posix_os} -d grains exec states

* "-t v" specifies that this is a vertically app-merged project
*  "-d grains exec states" says that we want to implement the dynamic names of "grains", "exec", and "states"

Add "idem-posix" to the requirements.txt::

    echo idem-posix >> requirements.txt

And that's it!  Go to town making grains, execution modules, and state modules specific to your posix os.
Follow the conventions you see in idem-posix.

For information about running idem states and execution modules check out
https://idem.readthedocs.io
