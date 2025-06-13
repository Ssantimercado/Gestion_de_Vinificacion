# C:\Users\Luciana\Desktop\proyecto_vino\Gestion_de_Vinificacion\routes\embotellado_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.embotellado_models import Embotellado  # Asegúrate de que esta importación sea correcta
from models.crianza_models import Crianza  # Asegúrate de que esta importación sea correcta
import datetime

embotellado_bp = Blueprint('embotellado', __name__)

@embotellado_bp.route('/embotellado/nuevo', methods=['GET', 'POST'])
def nuevo_embotellado():
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario (¡NOMBRES ACTUALIZADOS PARA COINCIDIR CON HTML!)
            fecha_str = request.form['fecha'] # Coincide con name="fecha" en form.html
            cantidad_botellas = int(request.form['cantidad_botellas'])
            crianza_id = request.form['crianza_id'] # Coincide con name="crianza_id" en form.html

            # NOTA: Tu HTML (form.html) no tiene campos para 'tipo_botella' ni 'notas'.
            # Tu modelo Embotellado sí tiene 'tipo_botella' (nullable=False) y 'notas' (nullable=True).
            # Si 'tipo_botella' es obligatorio y no lo pasas, Flask-SQLAlchemy lanzará un error.
            # Por eso, he añadido un valor provisional para 'tipo_botella'. Lo ideal es añadir un input en tu HTML.
            tipo_botella_valor = "Botella Estándar" # Valor provisional, considera añadirlo al formulario HTML
            notas_valor = request.form.get('notas', '') # Si agregas un campo 'name="notas"' en tu HTML, lo capturará, si no, será un string vacío.

            # Convertir la fecha de string a objeto date
            fecha_embotellado_obj = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()

            # Crear una nueva instancia de Embotellado
            nuevo = Embotellado(
                fecha_embotellado=fecha_embotellado_obj, # Nombre de la columna en tu modelo Embotellado
                cantidad_botellas=cantidad_botellas,
                crianza_id=crianza_id,
                tipo_botella=tipo_botella_valor,
                notas=notas_valor
            )

            # Agregar a la sesión y commitear a la base de datos
            db.session.add(nuevo)
            db.session.commit()
            flash('Embotellado registrado exitosamente!', 'success')
            return redirect(url_for('embotellado.nuevo_embotellado'))

        except Exception as e:
            db.session.rollback() # En caso de error, hacer rollback
            flash(f'Error al registrar el embotellado: {e}', 'danger')
            # Para depuración, puedes imprimir el error en la consola
            print(f"Error al procesar el formulario de embotellado: {e}")

    # Para el método GET o si hay un error en POST, cargar las crianzas
    crianzas = Crianza.query.all()
    # Asegúrate de que el url_for para el botón "Volver" apunte a donde debe ir.
    # Ya corregimos esto en form.html para que apunte a 'nuevo_embotellado'.
    return render_template('embotellado/form.html', crianzas=crianzas)