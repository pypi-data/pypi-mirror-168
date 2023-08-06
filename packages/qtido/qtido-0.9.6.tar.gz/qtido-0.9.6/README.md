
**qtido** est une bibliothèque Python(3) pour tracer des figures géométrique et faire des petits jeux.
Une sorte de documentation est disponible sur https://learn.heeere.com/python/reference-qtido/

Elle est basée sur les principes de conception et buts suivants :

- offrir une version de la biblothèque dans la langue de l'apprenant (le français ici, mais qtido est conçue pour être traduite),
- offrir une interface de programmation impérative sans "callback" ni asynchronisme apparent,
- permettre, entre autre, de faire des animations à interval de temp constant (si l'ordinateur est assez rapide),
- créer une abstraction qui permette un exécution des programmes aussi bien sur desktop (avec PyQt) que dans un navigateur (brython + implémentation en javascript de la bibliothèque)

Le nom est un mélange de *Qt* (composant graphiques utilisés par défaut) et de *ido* (langue universelle).

## Installation

~~~
pip install qtido
~~~

## Exemple simple

~~~python
from qtido import *

def mickey(fen, x, y, rayon):
    """Cette fonction trace un mickey"""
    couleur(fen, 1, 1, 1)     # Blanc
    disque(fen, x, y, rayon)  # cX, cY, rayon
    
    couleur(fen, 1, 0, 0)     # Rouge
    disque(fen, x+rayon/2, y-rayon, rayon/2 - 1)
    disque(fen, x-rayon/2, y-rayon, rayon/2 - 1)
    
    couleur(fen, 0, 0.7, 0)   # Vert
    disque(fen, x, y, rayon/5)


f = creer(400, 200)    # créer une fenêtre
mickey(f, 50, 50, 20)

mickey(f, 100, 50, 5)

mickey(f, 200, 50, 20)
mickey(f, 250, 50, 20)
mickey(f, 300, 50, 20)

mickey(f, 100, 120, 40)
mickey(f, 200, 120, 30)
mickey(f, 300, 120, 20)
mickey(f, 350, 120, 10)

attendre_fermeture(f)

~~~


----

## WIP and "feature requests"

- todo: check number of parameters and report if incorrect (how to reproduce?)
- todo: docstrings (localized)


## Notes

### generating a mapping and checking no ___ remains

    w=fr-fr ; ./apply-mapping.sh map-$w ; grep -Hrn '\(___\|%\)' $w/
    
### trying to get all a___ keys used, ordered safely

    cat abstract/*.py |grep ___|sed 's@a___@\na___@g' |grep ___|sed -e 's@.*\(a___[^-=,;:(). ]*\).*@\1@g' -e "s@'\$@@g" | awk '/^[^a]/ {printf "%05d %s\n", 0, $0 ; next} { printf "%05d %s\n", (99999-length($1)), $0 }' | sort | cut -d" " -f2-|uniq

## Teach

Packing the french version (with 3.2 python fix).

At the time of writting mnfy need 3.4 or older, and is un-maintained, so we'll use anaconda... (see the helper script commented lines...)

    w=fr-fr ; ./apply-mapping.sh map-$w && helper/build-minified.sh $w/ && (cd $w && zip -r ../qtido-$(date --rfc-3339=date).zip qtido.py minitest.py)
    w=fr-fr ; (cd $w && zip -r ../qtido-$(date --rfc-3339=date)-exemples.zip test-ex*.py)

## Teach to pypi

~~~
python3 -m pip install --upgrade setuptools wheel
python3 -m pip install --upgrade twine

# update the VERSION number in setup.py and then
rm -rf for-pypi
mkdir for-pypi
pushd for-pypi
mkdir qtido
cp ../fr-fr/qtido.py qtido/__init__.py
cp -t . ../setup.py ../README.md
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# OR (non-test): python3 -m twine upload dist/*

# try it
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps qtido
ll $VENV/lib/python3.9/site-packages/qtido
python3 -m pip uninstall qtido
ll $VENV/lib/python3.9/site-packages/qtido
python3 -m pip install  ..
ll $VENV/lib/python3.9/site-packages/qtido

popd

~~~

