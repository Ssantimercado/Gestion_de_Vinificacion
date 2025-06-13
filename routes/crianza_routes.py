from flask import Blueprint, render_template, request, redirect, url_for
from extensions import db  # ¡Importante! Aseguramos que use la misma instancia de DB
from models.crianza_models import Crianza
from models.variedad import VariedadUva
from models.fermentacion import Fermentacion
from models.recepcion import RecepcionUva # ¡¡¡NUEVO/CORREGIDO: Necesario para el join en buscar_crianza!!!
import datetime

# Definimos el Blueprint con el url_prefix correcto
crianza_bp = Blueprint('crianza', __name__, url_prefix='/crianza')

@crianza_bp.route('/nueva', methods=['GET', 'POST'])
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
        return redirect(url_for('crianza.listar_crianza'))

    # Necesitas pasar las fermentaciones para que el campo Select de Fermentacion_id funcione en el formulario
    fermentaciones = Fermentacion.query.all()
    return render_template('crianza/form.html', fermentaciones=fermentaciones)

@crianza_bp.route('/')
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

        # Filtrado: AHORA RecepcionUva está importada
        query = Crianza.query.join(Crianza.fermentacion).join(Fermentacion.recepcion).join(RecepcionUva.variedad)

        if tipo_recipient:
            query = query.filter(Crianza.tipo_recipient.ilike(f"%{tipo_recipient}%"))
        if variedad_id:
            query = query.filter(RecepcionUva.variedad_id == variedad_id)

        resultados = query.all()

    variedades = VariedadUva.query.all()
    return render_template('crianza/buscador.html', resultados=resultados,
                           tipo_recipient=tipo_recipient, variedad_id=variedad_id,
                           variedades=variedades)