Text Editor Plugins
===================

This directory contains the text editor plugins for the supported
editors, Atom, Emacs, Sublime, and Vim. Each plugin is unique and
features a unique installation process.

Installation
------------

Currently, installation of the plugins is done manually by following the
below instructions.

Atom
~~~~

-  Download and save the crossdoc-atom package to ``~/.atom/packages``
-  Reload or Launch Atom window, navigate to Packages where CrossDoc modules should be available.

Emacs
~~~~~

-  Download and save the ``emacs/CrossDoc.el`` file in your ``"~/.emacs.d/lisp"`` directory
-  Add the following lines to your ``~.emacs`` file

   -  ``(add-to-list 'load-path "~/.emacs.d/lisp")``
   -  ``(load "CrossDoc.el")``

-  The plugin will now auto-load on launching emacs

Sublime
~~~~~~~

-  Download and save the files in ``sublime`` to Sublime packages folder
   in a folder called ``CrossDoc``

   -  On Windows, this is in
      ``~/AppData/Roaming/Sublime Text 3/Packages/``

Vim
~~~

-  Download and save the ``vim/CrossDoc.vim`` file to your
   ``~/.vim/plugins/`` directory
