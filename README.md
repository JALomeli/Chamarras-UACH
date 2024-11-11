# Chamarras Universitarias - Sistema de Gestión de Pedidos

Este proyecto es una aplicación web que permite gestionar pedidos de chamarras universitarias. Incluye funcionalidades para registrar pedidos, generar gráficos estadísticos, enviar correos electrónicos y mensajes de WhatsApp a los clientes. 

## Instalación

Para ejecutar esta aplicación, asegúrate de tener Python y `pip` instalados en tu sistema. Luego, sigue estos pasos para instalar los requisitos necesarios:

1. Clona este repositorio o descarga los archivos en tu máquina local.
2. Ejecuta el siguiente comando en el directorio del proyecto para instalar las dependencias:

   ```bash
   pip install -r requirements.txt
Requisitos
Los siguientes módulos y librerías son necesarios para el funcionamiento de la aplicación:

Pandas: Para el manejo y análisis de datos.
Matplotlib: Para la generación de gráficos.
Flask: Framework de desarrollo web.
Flask-Mail: Para enviar correos electrónicos.
Pymongo: Para interactuar con la base de datos MongoDB.
PyWhatKit: Para enviar mensajes de WhatsApp.
Configuración
Crea un archivo .env con tus configuraciones, especialmente las credenciales de tu cuenta de Gmail y la URI de MongoDB.

En el archivo app.py, configura los parámetros de tu correo electrónico:

python
Copy code
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'tu_correo@gmail.com'
app.config['MAIL_PASSWORD'] = 'tu_contraseña'
Asegúrate de reemplazar tu_contraseña con la contraseña de la cuenta de correo electrónico o con una contraseña de aplicación si utilizas autenticación de dos factores en Gmail.

Ejecución de la Aplicación
Para iniciar la aplicación, ejecuta el siguiente comando:

bash
Copy code
python app.py
La aplicación estará disponible en http://127.0.0.1:5000 en tu navegador.

Funcionalidades
Gestión de Pedidos: Registro, visualización y eliminación de pedidos.
Estadísticas de Pedidos: Gráficos de cantidad de chamarras por color, talla y tipo de pago.
Mensajes: Envío de correos electrónicos y mensajes de WhatsApp a los clientes.
Políticas de Privacidad: Página para mostrar políticas de privacidad.
Notas Importantes
MongoDB: Debes tener acceso a una base de datos MongoDB para almacenar los pedidos.
WhatsApp: El envío de mensajes de WhatsApp requiere que tengas la versión web de WhatsApp iniciada en el navegador.
Dependencias
Para consultar todas las dependencias del proyecto, revisa el archivo requirements.txt.

Copy code

Este formato README en Markdown incluye todos los pasos y configuraciones necesarias para que el proyecto funcione correctamente.