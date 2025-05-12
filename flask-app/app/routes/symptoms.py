from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db

from app.forms import SymptomForm
from app.models import SymptomLog

symptoms_bp = Blueprint('symptoms', __name__)

@symptoms_bp.route('/symptoms/new', methods=['GET', 'POST'])
@login_required
def symptoms_new():
    form = SymptomForm()
    if form.validate_on_submit():
        entry = SymptomLog(
            user_id=current_user.id,
            symptoms=form.symptoms.data,
            medication=form.medication.data,
            medication_info=form.medication_info.data or None,
            relief=form.relief.data,
            relief_info=form.relief_info.data or None,
        )
        db.session.add(entry)
        db.session.commit()
        flash('Registro guardado con éxito.', 'success')
        return redirect(url_for('symptoms.symptoms_history'))

    return render_template('new_symptoms.html', form=form)

@symptoms_bp.route('/symptoms/history', methods=['GET'])
@login_required
def symptoms_history():
    symptoms = SymptomLog.query.filter_by(user_id=current_user.id).order_by(SymptomLog.datetime.desc()).all()
    return render_template('symptoms_history.html', symptoms=symptoms)

