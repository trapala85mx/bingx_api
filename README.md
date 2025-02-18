# bingx_api

Repositorio para conectarse y hacer uso de la API REST del exchange de Bingx así como los Websockets del mismo.

Este "conector de bingx" maneja un entorno asíncrono, por lo que se debe implementar en alguna función asíncrona.

Tiene implementadas algunos métodos pero se irán implementando a cómo lo vaya necesitando en los proyectos donde
interviene este repo.

Aún tiene detalles por mejorar como mejor manejo de Excepciones y, aún, hay un detalle al cerrar que se irá viendo.

---

Respository to connect and use Bingx API REST.

This "bingx connector" is developed in an asynchornus environment so, this must be used in a async method.

It has implemented some methods but they will be implemented as needed in the projects where this repo intervenes.

It still has details to improve such as better handling of Exceptions and, there is still a detail when closing that
will be seen.

# How to use
Este proyecto usa la libreria "uv" (https://docs.astral.sh/uv/getting-started/installation/) como manejador de ambiente
virtual. 

Lo que yo hice fue que, dentro de mi proyecto de trading_bot (creado con uv init) clone este repositorio.

Ya clonado elimine el .gitignore, REAMDE.md y el main.py. Con esto muevo a la raíz del proyecto el archivo pyproject.toml, sustituyendo el que se tiene por la creación del proyecto con "uv". 

Posterior, se modifica el nombre del proyecto dentro del "pyproject.toml" y se sincriniza con "uv sync" para que se actualice con la info del "pyproject.toml".

Se activa el entorno virtual.

---
This project uses the "uv" library (https://docs.astral.sh/uv/getting-started/installation/) as a virutal environment manager.

What I did was, within my trading_bot project (created with uv init) I cloned this repository.

Once cloned, delete the .gitignore, REAMDE.md and the main.py. With this I move the pyproject.toml file to the root of the project, replacing the one from the creation of the project with "uv".

Subsequently, the project name is modified within "pyproject.toml" and synchronized with "uv sync" so that it is updated with the "pyproject.toml" info.

Activate vrtual environment.
