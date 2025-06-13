# C:\Users\Luciana\Desktop\proyecto_vino\Gestion_de_Vinificacion\routes\embotellado_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models.embotellado_models import Embotellado  
from models.crianza_models import Crianza  
import datetime

embotellado_bp = Blueprint('embotellado', __name__)

@embotellado_bp.route('/embotellado/nuevo', methods=['GET', 'POST'])
def nuevo_embotellado():
    if request.method == 'POST':
        try:
            
            fecha_str = request.form['fecha'] # Coincide con name="fecha" en form.html
            cantidad_botellas = int(request.form['cantidad_botellas'])
            crianza_id = request.form['crianza_id'] # Coincide con name="crianza_id" en form.html
            tipo_botella_valor = "Botella Estándar" 
            notas_valor = request.form.get('notas', '') 

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
            db.session.rollback() 
            flash(f'Error al registrar el embotellado: {e}', 'danger')
            print(f"Error al procesar el formulario de embotellado: {e}")

    
    crianzas = Crianza.query.all()
    
    return render_template('embotellado/form.html', crianzas=crianzas)