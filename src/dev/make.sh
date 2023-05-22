py2applet --make-setup single-ep.py
rm -rf build dist
python setup.py py2app -A
open dist/single-ep.app/