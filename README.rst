Binkeul Code Editor 
============================
GUI application for editing and saving binkeul (constructed language) code and emoji

Install  
=======================
This program has been tested on Windows 10 and Python3.6.3. This can not guarantee to run in other environments.

Requirements
-----------------------

* PySide-1.2.4 : To install PySide-1.2.4 on Windows operating systems from Python 3.6, you need to download and install pyside whl from `<https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyside>` _ .

* peewee-3.3.4

* Pillow-5.1.0

* svgwrite-1.1.12


.. code-block:: none

    cd C:\Python36-32\Scripts

    pip3 install wheel
    ...
    wheel install PySide-1.2.4-cp36-cp36m-win32.whl
    ...
    pip3 install peewee
    ...
    pip3 install pillow
    ...
    pip3 install svgwrite
    ...


Copy Source 
---------------------------
Once the necessary package installation is complete, create a binkeul folder in Lib / site_packages in Python.3.6.x and copy the source from the repository.
        
.. code-block:: none
    
    cd C:\Python36-32\Lib\site-packages
    
    svn export https://github.com/sinabilo/binkeul/trunk/binkeul binkeul 

Run
----------------------
You can start the Binkeul Code Editor by executing the following command:
    
.. code-block:: none

    pythonw -m binkeul


Additional installation
========================
Although it is not absolutely necessary to run this program, the following programs and Python packages must be installed to use the ``betlsvg`` and ``betlsvgdir`` utilities.

* potrace 1.13

* CairoSVG-2.1.3



Reference 
==========================

* Introduction to the binkeul language : `<https://sites.google.com/site/binkeul>`_

* Help documentation for users of the Binkeul Code Editor : `<https://sites.google.com/site/binkeul/binkeuleditor>`_









    

