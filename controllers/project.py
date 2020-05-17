import os
from flask import request, Response, jsonify
from models.project import Project
from config.app import app
from datetime import datetime
import json
from slugify import slugify
from werkzeug.utils import secure_filename
from utils.constants import UPLOAD_FOLDER, UPLOAD_PATHNAME, ALLOWED_IMAGE_EXTENSIONS
from utils.utils import save_upload_path
import shutil

def allowed_image_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
           
@app.route('/projects')
def get_projects():
    try:
        args = request.args
        if "page" in args:
            page = int(args["page"])
        else:
            page = 1

        if "per_page" in args:
            per_page = int(args.get("per_page"))
        else:
            per_page = 15
            
        if "order_by" in args:
            order_by = args.get("order_by")
        else:
            order_by = "createdAt"
            
        
        projects = Project.objects.order_by(f"{order_by}")
        paginated_projects = projects.paginate(page=page, per_page=per_page)

        return jsonify({
                "items": paginated_projects.items, 
                "current_page": paginated_projects.page, 
                "per_page": paginated_projects.per_page, 
                "total": paginated_projects.total, 
            }), 200
    except Exception as e:
        print(e)

@app.route('/projects', methods=['POST'])
def add_project():
    try:
        body = request.get_json()
        file = request.files['image']
        name = request.form['name']

        if file and allowed_image_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(save_upload_path(UPLOAD_FOLDER, filename))
            
            # files = []
            # for filename in os.listdir(UPLOAD_FOLDER):
            #     path = os.path.join(UPLOAD_FOLDER, filename)
            #     if os.path.isfile(path):
            #         files.append(filename)
            # return jsonify(files)
            
            
            project =  Project(name=name)
            project.slug = slugify(project.name)
            project.image = UPLOAD_PATHNAME+filename
            project._image_file.put(file, content_type=file.content_type)
            project.save()
        return jsonify(project), 200
        
        project =  Project(**body)
        project.slug = slugify(project.name)
        project.save()

        return jsonify(project), 200
    except Exception as e:
            print(e)

@app.route('/projects/<id>', methods=['PUT'])
def update_project(id):
    try:
        body = request.get_json()
        project = Project.objects.get(id=id)
        project.update(**body, updatedAt = datetime.now(), slug = slugify(body['name']))
        project.reload()
        return jsonify(project), 200
    except Exception as e:
        print(e)

@app.route('/projects/<id>', methods=['DELETE'])
def delete_project(id):
    try:
        project = Project.objects.get_or_404(id=id).delete()

        return { "id": id }, 200
    except Exception as e:
            print(e)

@app.route('/projects/<id>')
def get_project(id):
    try:
        project = Project.objects.get_or_404(id=id).to_json()

        return Response(project, mimetype="application/json", status=200)
    except Exception as e:
        print(e)

@app.route('/projects/slug/<slug>')
def get_project_by_slug(slug):
    try:
        project = Project.objects.get_or_404(slug=slug).to_json()

        return Response(project, mimetype="application/json", status=200)
    except Exception as e:
        print(e)

@app.route('/projects', methods=['DELETE'])
def delete_projects():
    try:
        project = Project.objects.delete()
        if os.path.isDir(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
        return { "status": "success"}, 200
    except Exception as e:
        print(e)