# Software-Design-2021

## Requerimientos para el desarrollo del proyecto

* Tener [python](https://www.python.org/downloads/windows/) >= 3.9.1 instalado.
* Tener [git](https://git-scm.com/downloads) instalado de manera local.
* Tener [Postgres 14](https://www.postgresql.org/download/windows/) instalado (asegurarse que también se instale PgAdmin 4).

## Pasos iniciales

* Clonar el repositorio<br/>
En alguna carpeta local, abrir git bash y insertar el siguiente comando:
```
git clone https://github.com/alessioghio/software-design-2021.git
```

* Instalar el módulo "pipenv" con el siguiente comando
```
pip install pipenv
```

* Crear un *virtual environment* con pip env
```
pipenv shell
```
**Nota:<br />-Para entrar al virtual environment, a través de Visual Studio Code, se tiene que presionar ctrl+shift+p y en la barra de búsqueda seleccionar "Python: Select Interpreter" y el *virtual environment*.<br />-Para salir del *virtual environment*, se puede ingresar en el terminal "exit".**

* Dentro del *virtual environment*, instalar todos los módulos del archivo **requirements.txt**
```
pip install -r requirements.txt
```

## Recomendaciones

* En su git local crear un *branch* para el desarrollo que se distinga del *main*.