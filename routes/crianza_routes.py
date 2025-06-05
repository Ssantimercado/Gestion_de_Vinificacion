from flask import Blueprint, render_template, request, redirect, url_for
from models.db import db
from models.crianza_models import Crianza
from models.variedad import VariedadUva
from models.fermentacion import Fermentacion
import datetime

crianza_bp = Blueprint('crianza', __name__)

@crianza_bp.route('/crianza/nueva', methods=['GET', 'POST'])
def crear_crianza():
    if request.method == 'POST':
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        tipo_recipient = request.form['tipo_recipient']
        observaciones = request.form['observaciones']
        fermentacion_id = request.form['fermentacion_id']

        nueva_crianza = Crianza(
            fecha_inicio=datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d").date(),
            fecha_fin=datetime.datetime.strptime(fecha_fin, "%Y-%m-%d").date() if fecha_fin else None,
            tipo_recipient=tipo_recipient,
            observaciones=observaciones,
            fermentacion_id=fermentacion_id
        )

        db.session.add(nueva_crianza)
        db.session.commit()
        return redirect(url_for('crianza.listar_crianza'))  # Ruta que muestra la lista

    return render_template('crianza/form.html')

@crianza_bp.route('/crianza')
def listar_crianza():
    crianzas = Crianza.query.all()
    return render_template('crianza/lista.html', crianzas=crianzas)

@crianza_bp.route('/buscar', methods=['GET', 'POST'])
def buscar_crianza():
    resultados = []
    tipo_recipient = ""
    variedad_id = ""

    if request.method == 'POST':
        tipo_recipient = request.form.get('tipo_recipient', '')
        variedad_id = request.form.get('variedad_id', '')

        # Filtrado
        query = Crianza.query.join(Crianza.fermentacion).join(Fermentacion.variedad)

        if tipo_recipient:
            query = query.filter(Crianza.tipo_recipient.ilike(f"%{tipo_recipient}%"))
        if variedad_id:
            query = query.filter(Fermentacion.variedad_id == variedad_id)

        resultados = query.all()

    variedades = Variedad.query.all()
    return render_template('crianza/buscador.html', resultados=resultados,
                           tipo_recipient=tipo_recipient, variedad_id=variedad_id,
                           variedades=variedades)