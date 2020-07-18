import os
from flask import (
    Flask,
    request,
    jsonify,
    abort,
    request,
    Response
)
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import setup_db, Artist, Video
from .auth.auth import AuthError, requires_auth, get_token_auth_header

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    '''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
    db_drop_and_create_all()

# ===================
# ROUTES
# ===================


    @app.route('/artists')
    def get_artists():

        artists = Artist.query.all()

        if len(artists) == 0:
            print("test works, no artists found")
            abort(401)

        return jsonify({
            'success': True,
            'artists': "Test works, someone is found"
        })

    @app.route('/videos')
    def get_videos():
        videos = Video.query.all()

        if len(videos) == 0:
            print("test works, no videos found")
            abort(401)

        return jsonify({
            'success': True,
            'artists': "Test works, one video is found"
        })

    return app
    
APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

# =================================================================
#  Error Handlers
# =================================================================
'''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'Unathorized'
        }), 401

    @app.errorhandler(404)
    def unreachable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Server Error'
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(auth):
        a_error = jsonify(auth.error)
        a_error.status_code = auth.status_code
        return a_error
'''