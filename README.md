# 🛒 Mi Tienda - Aplicación Web de Venta de Productos
# Descripción

Mi Tienda es una aplicación web desarrollada en Django para el backend y Tailwind CSS para el frontend, que permite gestionar un comercio en línea de productos (ropa, calzado, alimentos, etc.).
La aplicación incluye funcionalidades para:

Login y gestión de usuarios.

Gestión de categorías y productos.

Carrito de compras con cálculo automático de precios e IVA.

Gestión de pedidos y estado de pago.

Visualización de productos y categorías desde el home.

La base de datos se maneja con MySQL y se puede ejecutar localmente usando XAMPP o cualquier servidor MySQL compatible.

# Estructura de la Aplicación
mi_tienda/
├── products/         # App de productos y categorías
├── cart/             # App de carrito de compras
├── orders/           # App de pedidos
├── users/            # App de usuarios y autenticación
├── templates/        # Plantillas HTML
├── static/           # Archivos CSS, JS y assets
├── mi_tienda/        # Configuración de Django
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    ...
└── manage.py

# Funcionalidades Clave
# Usuarios

Registro y login de usuarios.

Perfil con teléfono y dirección.

Gestión de sesiones para carrito.

# Productos

Crear, editar y eliminar productos.

Asociar productos a categorías.

Visualizar precio con IVA calculado automáticamente.

Subida opcional de imagen de producto.

# Categorías

Crear, editar y eliminar categorías.

Ver productos asociados a cada categoría.

# Carrito de Compras

Agregar productos y cantidades al carrito.

Actualizar cantidades y eliminar productos.

Calcular total con IVA en tiempo real.

# Pedidos

Crear pedidos a partir del carrito.

Guardar histórico de pedidos con estado y método de pago.

Calcular subtotal, IVA y total automáticamente.

# Requisitos

Python 3.10 o superior

Django 4.x

MySQL / MariaDB

Tailwind CSS (integrado en templates)
# nota: en caso tal de tener errores para instalar tailwindcss e iniciarlo, lo recomendable es instalar una version anterior a la actual.

Librerías Python adicionales (requeridas en requirements.txt):

django
mysqlclient
Pillow

# Instalación y Ejecución

Clonar el repositorio:

git clone <URL-del-repositorio>
cd mi_tienda


Crear un entorno virtual:

python -m venv mi_tienda_env
source mi_tienda_env/bin/activate  # Linux/Mac
mi_tienda_env\Scripts\activate     # Windows


# Instalar dependencias:

pip install -r requirements.txt


# Configurar la base de datos en settings.py (MySQL):

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mi_tienda_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}


Cargar script de base de datos:

# Desde phpMyAdmin o MySQL CLI
source database_script.sql;


# Ejecutar migraciones y crear superusuario:

python manage.py migrate
python manage.py createsuperuser


# Ejecutar servidor:

python manage.py runserver

# Pruebas Unitarias

Se incluyen pruebas unitarias para:

Productos (products/tests.py)

Carrito (cart/tests.py)

Pedidos (orders/tests.py)

Usuarios (users/tests.py)

Ejecutar tests:

python manage.py test


# ⚠ Nota: Las pruebas usan los modelos tal como están definidos; asegúrate de que los campos coincidan.

Consideraciones Importantes

MariaDB Strict Mode: Se recomienda activar Strict Mode en MySQL/MariaDB para evitar problemas de integridad de datos.

Rutas de imágenes: Las imágenes de productos se guardan en MEDIA_ROOT/products/. Configurar MEDIA_URL y MEDIA_ROOT en settings.py.

Microservicios: Actualmente la app está monolítica; cada módulo (productos, carrito, pedidos) es independiente pero dentro de Django.

Seguridad: Para producción, configurar correctamente DEBUG=False y ALLOWED_HOSTS.

Tailwind CSS: Se puede compilar localmente si se hacen cambios en los estilos, siguiendo la documentación oficial de Tailwind.
