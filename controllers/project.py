import os
from flask import request, Response, jsonify
from models.project import Project
from config.app import app
from datetime import datetime
import json
from slugify import slugify
from werkzeug.utils import secure_filename
from utils.constants import UPLOAD_FOLDER, UPLOAD_PATHNAME, ALLOWED_IMAGE_EXTENSIONS, BASE_DIR
from utils.utils import save_upload_path, remove_contents, remove_uploaded_file, rename_filename

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
        images = request.files.to_dict(flat=False)['images']

        if not file or not allowed_image_file(file.filename):
            return { "error": "only image can be uploaded"}, 200

        filename = rename_filename('pimg-'+name, file.filename)
        file.save(save_upload_path(UPLOAD_FOLDER, filename))
        
        files = []
        if images:
            for image in images:
                image_filename = rename_filename('pimgs-'+name, image.filename)
                image.save(save_upload_path(UPLOAD_FOLDER, image_filename))

                files.append(UPLOAD_PATHNAME+image_filename)
       
        project =  Project(name=name)
        project.slug = slugify(project.name)
        project.image = UPLOAD_PATHNAME+filename
        project.images = files
        project.save()
            
        return jsonify(project), 200
        
    except Exception as e:
        print(e)

@app.route('/projects/<id>', methods=['PUT'])
def update_project(id):    
    try:
        name = request.form['name']
        project = Project.objects.get(id=id)
        
        if request.files:
            file = request.files['image']
            
            currentImage = project.image
            filename = rename_filename('edited-pimg-'+name, file.filename)
            path_filename = UPLOAD_PATHNAME+filename
            if file and allowed_image_file(file.filename):
                formatted_img = currentImage.split('_')[-1]
                if not formatted_img in file.filename:
                    remove_uploaded_file(currentImage)
                
                file.save(save_upload_path(UPLOAD_FOLDER, filename))
                
        
            project.update(name = name, updatedAt = datetime.now(), slug = slugify(name), image=path_filename)
            project.reload()
            return jsonify(project), 200
        
        project.update(name = name, updatedAt = datetime.now(), slug = slugify(name))
        project.reload()
        return jsonify(project), 200
        
    except Exception as e:
        print(e)

@app.route('/projects/images/<id>', methods=['PUT'])
def update_images_project(id):    
    try:
        project = Project.objects.get(id=id)
        
        images = request.files.to_dict(flat=False)['images']
        # requim = request.files['images']
        
        files = []
        currentImages = project.images
        
        for project_image in currentImages:
            remove_uploaded_file(project_image)
            
        for image in images:
            image_filename = secure_filename(image.filename)
            saved_pathname = rename_filename('edited-pimgs-'+project.slug, image_filename)
            files.append(saved_pathname)
            
            image.save(save_upload_path(UPLOAD_FOLDER, saved_pathname))
    
        project.update(updatedAt = datetime.now(), images=files)
        project.reload()
        return jsonify(project), 200   
        
    except Exception as e:
        print(e)

@app.route('/projects/<id>', methods=['DELETE'])
def delete_project(id):
    try:
        project = Project.objects.get_or_404(id=id)
        remove_uploaded_file(project.image)
        
        for image in project.images:
            remove_uploaded_file(image)
                   
        project.delete()

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
        remove_contents(UPLOAD_FOLDER)

        return { "status": "success"}, 200
    except Exception as e:
        print(e)