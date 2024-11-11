

import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask
from flask_mail import Mail, Message
import pywhatkit as kit
import time


app = Flask(__name__)
mail = Mail(app)
app.secret_key = 'c'  
uri = ""
client = MongoClient(uri, server_api=ServerApi("1"))
db = client['pedidos_chamarras']
coleccion_pedidos = db['pedidos']

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Servidor SMTP 
app.config['MAIL_PORT'] = 465  # Puerto para SSL
app.config['MAIL_USE_SSL'] = True  # Usar SSL para la conexión
app.config['MAIL_USERNAME'] = 'chamarrasuniversitarias7@gmail.com'  # Tu dirección de correo electrónico
app.config['MAIL_PASSWORD'] = 'chamarraazul'  # Tu contraseña de correo electrónico (si usas Gmail, puede ser una contraseña de aplicación)
app.config['MAIL_DEFAULT_SENDER'] = 'chamarrasuniversitarias7@gmail.com'  # Dirección predeterminada para los correos enviados

class FormularioPedido:
    def __init__(self, nombre_usuario, correo, telefono, matricula, color, talla, nombre_personalizado, numero_deposito, tipo_pago):
        self.nombre_usuario = nombre_usuario
        self.correo = correo
        self.telefono = telefono
        self.matricula = matricula
        self.color = color
        self.talla = talla
        self.nombre_personalizado = nombre_personalizado
        self.numero_deposito = numero_deposito
        self.tipo_pago = tipo_pago

    def guardar_pedido(self):
        coleccion_pedidos.insert_one({
            "nombre_usuario": self.nombre_usuario,
            "correo": self.correo,
            "telefono": self.telefono,
            "matricula": self.matricula,
            "color": self.color,
            "talla": self.talla,
            "nombre_personalizado": self.nombre_personalizado,
            "numero_deposito": self.numero_deposito,
            "tipo_pago": self.tipo_pago
        })


    def mostrar_pedidos():
        return list(coleccion_pedidos.find())
    
    def contar_chamarras_por_color():

        pedidos = list(coleccion_pedidos.find())
        df = pd.DataFrame(pedidos)
        conteo_colores = df['color'].value_counts()
        return conteo_colores.to_dict()
    
    def contar_chamarras_por_talla():
        pedidos = list(coleccion_pedidos.find())
        df = pd.DataFrame(pedidos)
        conteo_tallas = df['talla'].value_counts() 
        return conteo_tallas.to_dict()  

    def contar_pedidos_por_pago():
        pedidos = list(coleccion_pedidos.find())
        df = pd.DataFrame(pedidos)
        conteo_pago = df['tipo_pago'].value_counts() 
        return conteo_pago.to_dict()  
    
    def sumar_depositos():
        pedidos = list(coleccion_pedidos.find())
        total_depositos = sum(
            int(pedido.get('numero_deposito', 0)) if pedido.get('numero_deposito', '').isdigit() else 0
            for pedido in pedidos
        )
        return total_depositos
    
    def contar_total_pedidos():
        pedidos = list(coleccion_pedidos.find())
        total_pedidos = len(pedidos)
        
        return total_pedidos
    
    def eliminar_pedido(nombre_usuario):
        resultado = coleccion_pedidos.delete_one({"nombre_usuario": nombre_usuario})
        if resultado.deleted_count > 0:
            return True  
        else:
            return False  




@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        correo = request.form['correo']
        telefono = request.form['telefono']
        matricula = request.form['matricula']
        color = request.form.get('color')
        talla = request.form.get('talla')
        nombre_personalizado = request.form['nombre_personalizado']
        numero_deposito = request.form['numero_deposito']
        tipo_pago = request.form.get('tipo_pago')

        datos_formulario = FormularioPedido(
            nombre_usuario, correo, telefono, matricula, color, talla, nombre_personalizado, numero_deposito, tipo_pago
        )
        datos_formulario.guardar_pedido()

        flash("Pedido realizado con éxito", 'success')

        mensaje = f"""
        ¡Gracias por tu pedido, {nombre_usuario}!

        Detalles de tu pedido:
        - Nombre: {nombre_usuario}
        - Correo: {correo}
        - Teléfono: {telefono}
        - Matrícula: {matricula}
        - Color: {color}
        - Talla: {talla}
        - Nombre Personalizado: {nombre_personalizado}
        - Número de Depósito: {numero_deposito}
        - Tipo de Pago: {tipo_pago}

        ¡Tu pedido está siendo procesado!

        Atentamente,
        Chamarras Universitarias FING
        """

        try:
            kit.sendwhatmsg_instantly(f'+52{telefono}', mensaje)
            flash("Pedido realizado con éxito. Recibirás un mensaje de WhatsApp con los detalles.", 'success')
        except Exception as e:
            flash(f"Error al enviar el mensaje de WhatsApp: {str(e)}", 'danger')
            
        return redirect(url_for('inicio'))
    return render_template('formulario.html')


@app.route("/privacidad")
def privacidad():
    return render_template("privacidad.html")

@app.route('/inventario')
def inventario():
    pedidos = FormularioPedido.mostrar_pedidos()
    return render_template('inventario.html', pedidos=pedidos)

@app.route('/eliminar_pedido', methods=['POST'])
def eliminar_pedido():
    nombre_usuario = request.form['nombre_usuario']  
    if FormularioPedido.eliminar_pedido(nombre_usuario):
        flash(f"Pedido de {nombre_usuario} eliminado con éxito", 'success')
    else:
        flash(f"No se encontró un pedido con el nombre {nombre_usuario}", 'danger')
    return redirect(url_for('inventario'))

@app.route("/graficas")
def graficas():
    conteo_colores = FormularioPedido.contar_chamarras_por_color()
    conteo_tallas = FormularioPedido.contar_chamarras_por_talla()
    conteo_pago = FormularioPedido.contar_pedidos_por_pago()
    total_depositos = FormularioPedido.sumar_depositos() 
    total_pedidos = FormularioPedido.contar_total_pedidos()

    colores = list(conteo_colores.keys())  
    cantidades_colores = list(conteo_colores.values())  
    tallas = list(conteo_tallas.keys())  
    cantidades_tallas = list(conteo_tallas.values())  

    tipos_pago = list(conteo_pago.keys())  
    cantidades_pago = list(conteo_pago.values())  


    fig, ax = plt.subplots(1, 3, figsize=(18, 6)) 


    ax[0].bar(colores, cantidades_colores, color=['pink', 'blue'])
    ax[0].set_xlabel('Color de Chamarras')
    ax[0].set_ylabel('Cantidad')
    ax[0].set_title('Cantidad de Chamarras Azules vs Rosas')


    for i, cantidad in enumerate(cantidades_colores):
        ax[0].text(i, cantidad / 2, f'{cantidad}', ha='center', va='center', fontsize=12, color='white', bbox=dict(facecolor='black', edgecolor='none', boxstyle='round,pad=0.3'))

  
    ax[1].bar(tallas, cantidades_tallas, color=['green', 'orange', 'red', 'purple', 'yellow'])
    ax[1].set_xlabel('Talla de Chamarras')
    ax[1].set_ylabel('Cantidad')
    ax[1].set_title('Cantidad de Chamarras por Talla')

    for i, cantidad in enumerate(cantidades_tallas):
        ax[1].text(i, cantidad / 2, f'{cantidad}', ha='center', va='center', fontsize=12, color='white', bbox=dict(facecolor='black', edgecolor='none', boxstyle='round,pad=0.3'))


    ax[2].bar(tipos_pago, cantidades_pago, color=['purple', 'blue'])
    ax[2].set_xlabel('Tipo de Pago')
    ax[2].set_ylabel('Cantidad')
    ax[2].set_title('Cantidad de Chamarras por Tipo de Pago')


    for i, cantidad in enumerate(cantidades_pago):
        ax[2].text(i, cantidad / 2, f'{cantidad}', ha='center', va='center', fontsize=12, color='white', bbox=dict(facecolor='black', edgecolor='none', boxstyle='round,pad=0.3'))


    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()  

    return render_template("graficas.html", img_data=img_base64, total_depositos=total_depositos, total_pedidos=total_pedidos)


@app.route('/acciones')
def acciones():
    return render_template('acciones.html')

@app.route('/enviar_mensaje', methods=['POST'])
def enviar_mensaje():
    asunto = request.form['asunto']
    mensaje = request.form['mensaje']

    destinatarios = [pedido['correo'] for pedido in coleccion_pedidos.find()]

    try:
        msg = Message(asunto, recipients=destinatarios)
        msg.body = mensaje

        mail.send(msg)
        flash("Correo enviado con éxito")
        return redirect(url_for('acciones'))
    except Exception as e:
        flash(f"Error al enviar el correo: {str(e)}", 'danger')
        return redirect(url_for('acciones'))

@app.route('/enviar_whatsapp', methods=['POST'])
def enviar_whatsapp():
    mensaje = request.form['mensaje']  
    numeros_telefonos = [pedido['telefono'] for pedido in coleccion_pedidos.find()]
    numeros_telefonos = [f'+52{numero}' for numero in numeros_telefonos]  
    
    try:
        for numero in numeros_telefonos:
            kit.sendwhatmsg_instantly(numero, mensaje)
            time.sleep(8)
        flash("Mensaje enviado con éxito a WhatsApp", 'success')
    except Exception as e:
        flash(f"Error al enviar el mensaje: {str(e)}", 'danger')

    return redirect('/acciones')


if __name__ == '__main__':
    app.run(debug=True)
