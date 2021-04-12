from flask import Blueprint, flash, render_template, request, redirect, send_from_directory, abort, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from . import db
import os
from .models import *

# creates the non related auth app
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    file_list = File.query.all()
    return render_template('profile.html', name=current_user.name, file_list=file_list)


@main.route('/uploader', methods=['POST'])
@login_required
def uploader():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        my_file = request.files['file']
        if my_file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if my_file:
            filename = secure_filename(my_file.filename)
            path_to_file = os.path.join(
                current_app.config['UPLOAD_FOLDER'], filename)
            # stores the file in the server
            my_file.save(path_to_file)
            size = os.stat(path_to_file).st_size
            # Upload to database
            file_in_db = File(name=filename, size=f"{size}bytes")
            db.session.add(file_in_db)
            db.session.commit()
        return redirect('/profile')


@ main.route('/download/<int:file_id>')
@ login_required
def download(file_id):
    try:
        file_to_download_name = File.query.get(file_id).name
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], file_to_download_name, as_attachment=True)
    except:
        abort(404)


@ main.route('/delete/<int:file_id>')
@ login_required
def delete(file_id):
    if current_user.admin:
        file_to_erase = File.query.get(file_id)
        os.remove(os.path.join(
            current_app.config['UPLOAD_FOLDER'], file_to_erase.name))
        db.session.delete(file_to_erase)
        db.session.commit()
    else:
        flash('You have to be an admin to delete files')
    return redirect('/profile')
