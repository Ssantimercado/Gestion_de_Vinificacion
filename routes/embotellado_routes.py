from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.db import db
from models.embotellado_models import Embotellado
from models.crianza_models import Crianza
from datetime import datetime

embotellado_bp = Blueprint('embotellado', __name__, url_prefix='/embotellado')

@embotellado_bp.route('/')
def lista_embotellado():
    embotellados = Embotellado.query.all()
    return render_template('embotellado/lista.html', embotellados=embotellados)

@embotellado_bp.route('/nuevo', methods=['GET', 'POST'])
def nuevo_embotellado():
    if request.method == 'POST':
        fecha = request.form.get('fecha')
        cantidad_botellas = request.form.get('cantidad_botellas')
        crianza_id = request.form.get('crianza_id')

        nuevo = Embotellado(
            fecha=datetime.strptime(fecha, '%Y-%m-%d'),
            cantidad_botellas=int(cantidad_botellas),
            crianza_id=crianza_id
        )

        db.session.add(nuevo)
        db.session.commit()
        flash('Embotellado registrado con éxito.')
        return redirect(url_for('embotellado.lista_embotellado'))

    crianzas = Crianza.query.all()
    return render_template('embotellado/form.html', crianzas=crianzas)
