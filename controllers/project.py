from flask import request, Response, jsonify
from models.project import Project
from config.app import app
from datetime import datetime
import json

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
        project =  Project(**body).save()

        return jsonify(project), 200
    except Exception as e:
            print(e)

@app.route('/projects/<id>', methods=['PUT'])
def update_project(id):
    try:
        body = request.get_json()
        project = Project.objects.get(id=id)
        project.update(**body, updatedAt = datetime.now())
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

@app.route('/projects', methods=['DELETE'])
def delete_projects():
    try:
        project = Project.objects.delete()
        return { "status": "success"}, 200
    except Exception as e:
        print(e)