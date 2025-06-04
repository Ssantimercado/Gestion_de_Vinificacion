from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.db import db
from models.crianza_models import Crianza
from models.fermentacion import Fermentacion
from datetime import datetime

crianza_bp = Blueprint('crianza', __name__, url_prefix='/crianza')

@crianza_bp.route('/')
def lista_crianza():
    crianzas = Crianza.query.all()
    return render_template('crianza/lista.html', crianzas=crianzas)

@crianza_bp.route('/nueva', methods=['GET', 'POST'])
def nueva_crianza():
    if request.method == 'POST':
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin') or None
        tipo_recipient = request.form.get('tipo_recipient')
        observaciones = request.form.get('observaciones')
        fermentacion_id = request.form.get('fermentacion_id')

        nueva = Crianza(
            fecha_inicio=datetime.strptime(fecha_inicio, '%Y-%m-%d'),
            fecha_fin=datetime.strptime(fecha_fin, '%Y-%m-%d') if fecha_fin else None,
            tipo_recipient=tipo_recipient,
            observaciones=observaciones,
            fermentacion_id=fermentacion_id
        )

        db.session.add(nueva)
        db.session.commit()
        flash('Crianza registrada con éxito.')
        return redirect(url_for('crianza.lista_crianza'))

    fermentaciones = Fermentacion.query.all()
    return render_template('crianza/form.html', fermentaciones=fermentaciones)
