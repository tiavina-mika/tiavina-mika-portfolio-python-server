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
            page = args["page"]

        if "per_page" in args:
            per_page = args.get("per_page")
        
        projects = Project.objects.order_by('-createdAt')
        paginated_projects = projects.paginate(page=int(page) or 1, per_page=int(per_page) or 2)

        return jsonify({
                "items": paginated_projects.items, 
                "current_page": paginated_projects.page, 
                "per_page": paginated_projects.per_page, 
                "total": paginated_projects.total, 
            }), 200
    except Exception as e:
        print(e)

# @app.route('/projects')
# def get_projects():
#     try:
#         body = request.get_json()
#         projects = Project.objects.order_by('-createdAt')
#         page = body.get('current_page') or 1
#         per_page = body.get('per_page') or 2
#         paginated_projects = projects.paginate(page=int(page), per_page=int(per_page))

#         return jsonify({
#                 "items": paginated_projects.items, 
#                 "current_page": paginated_projects.page, 
#                 "per_page": paginated_projects.per_page, 
#                 "total": paginated_projects.total, 
#             }), 200
#     except Exception as e:
#         print(e)

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
        Project.objects.get(id=id).update(**body, updatedAt = datetime.now())
        return Project.objects().to_json(), 200
    except Exception as e:
        print(e)

@app.route('/projects/<id>', methods=['DELETE'])
def delete_project(id):
    try:
        project = Project.objects.get(id=id).delete()
        return '', 200
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