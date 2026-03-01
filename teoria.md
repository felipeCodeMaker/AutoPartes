# En el "models.py" creamos tantas clases como tablas vaya a tener nuestra BBDD, para esta App.
# En el "settings.py" añadimos nuestra App en la lista de "INSTALED APPS"

# Para comprobar si hay algun problema en nuestro código:
python manage.py check InicioSesion

# Para crear la BBDD vacía (esto nos devuelve un nº de migración, por ejemplo 0001)
python manage.py makemigrations

# Para generar las tablas definidas en el "models.py" (debemos indicar el nº de miración anterior):
python manage.py sqlmigrate InicioSesion 0001

# Para incorportar esas tablas a nuestra BBDD:
python manage.py migrate