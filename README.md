<h1 align="center"> Rubisen Mappy <br></h1>
<div align="center">
  <h3>📦📦</h3>
  <p>Rubisen python keyboard mapper</p>
</div>



# Introduction

Le programme FinalCube permet de rendre possible l'utilisation d'un supercube i3s comme une entrée clavier sur  Windows.

Plus précisément, le programme permet d'attribuer un mouvement du cube xiaomi i3s à une touche du clavier, pour simuler sa pression.

# Usage

###### Windows usage

* Download the zip folder [latest build](https://github.com/JulesMicho/rubisenMappy/releases)
* Execute rubisenMappy.exe

###### Project setup
```console
pip install -r requirements.txt --user
```

###### Project run
```
run rubisenMappy.exe file
```

# Build

###### Windows
```console
pyinstaller -F --add-data BleakUWPBridge.dll;. finalcube.py
```

# Tips

Quelquefois, il se peut que la connexion bluetooth échoue.
Vous pouvez essayer :

* Vérifier que l'option bluetooth est activée sous windows.
* Recharger le cube.
* Se connecter manuellement avec windows au cube ( bluetooth  > Ajouter un appareil bluetooth ou un autre appareil > clique sur le device bluetooth )

