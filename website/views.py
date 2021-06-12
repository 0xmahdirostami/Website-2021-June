from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template("home.html",user=current_user)
@views.route('/projects/standford-covid')
def stanford():
    return render_template("standford-covid.html",user=current_user)
@views.route('/projects/pacman')
def pacman():
    return render_template("pacman.html",user=current_user)

@views.route('/apis')
def apis():
    return render_template("apis.html",user=current_user)
@views.route('/websites')
def websites():
    return render_template("websites.html",user=current_user)


@views.route('/note', methods=['GET', 'POST'])
@login_required
def note():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("note.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

