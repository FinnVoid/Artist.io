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

from models import setup_db, Artist, Video
from auth.auth import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


def create_app(test_config=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
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

    # db_drop_and_create_all()

    # ===================
    # ROUTES
    # ===================

    @app.route('/')
    def get_greeting():
        return "Salutations Comrade. No front end created yet. see README.md"

    # =============
    # Artists :
    # =============

    @app.route('/artists')
    def get_artists():

        artists = Artist.query.all()

        if len(artists) == 0:
            return "No artists are currently availble, please try adding one!"
            print("No Artists Found")
            abort(401)

        return jsonify({
            'success': True,
            'artists': [artist.format() for artist in artists]
        })

    # Post New Artist

    @app.route('/artists', methods=['POST'])
    def create_artist():

        body = request.json

        artist_name = body['name']
        artist_age = body['age']
        artist_style = body['style']

        try:
            new_artist = Artist(
                name=artist_name, age=artist_age, style=artist_style)
            print('Post initialized')
            new_artist.insert()

        except Exception as e:
            print(e)
            print("something went wrong")
            print(e.args)
            abort(400)

        return jsonify({
            "success": True,
            "artists": new_artist.format()
        }), 200

    # See single Artist info

    @app.route('/artists/<int:id>')
    def get_artist_by_id(id):
        try:
            artists = Artist.query.get(id)
            response = artists.format()
        except:
            abort(404)

        return jsonify({
            'success': True,
            'artists': response
        })

    # Update single Artist info

    @app.route('/artists/<int:id>', methods=['PATCH'])
    @requires_auth('patch:artist')
    def edit_artist_by_id(payload, id):
        
        body = request.json
        print(payload)
        artist_id = id
        artist = Artist.query.filter_by(id=artist_id).one_or_none()

        if artist is None:
            abort(404)

        if 'name' in body:
            artist.name = body['name']

        if 'style' in body:
            artist.style = body['style']

        if 'age' in body:
            artist.age = body['age']

        try:
            artist.insert()

        except Exception:
            abort(400)

        return jsonify({
            'success': True,
            'artists': artist.format()
        })

    # Delete single Artist by ID

    @app.route('/artists/<int:id>', methods=['DELETE'])
    @requires_auth('delete:artist')
    def delete_artist_by_id(payload, id):
        artist = Artist.query.filter_by(id=id).one_or_none()

        if not artist:
            abort(404)

        try:
            artist.delete()
        except:
            abort(400)

        return jsonify({
            'success': True,
            'delete': id
        }), 200

    # =============
    # Videos :
    # =============

    @app.route('/videos')
    def get_videos():
        videos = Video.query.all()

        if len(videos) == 0:
            return "No Videos are currently availble, please try adding one!"
            print("No Videos Found")
            abort(401)

        return jsonify({
            'success': True,
            'videos': [video.format() for video in videos]
        })

    @app.route('/add-videos', methods=['POST'])
    @requires_auth('post:video')
    def create_video(payload):

        body = request.json

        video_title = body['title']
        video_type = body['type']

        try:
            new_video = Video(
                title=video_title, type=video_type)
            print('Post initialized')
            new_video.insert()


        except Exception as e:
            print(e)
            print("something went wrong")
            print(e.args)
            abort(400)

        return jsonify({
            "success": True,
            "videos": new_video.format()
        }), 200

    @app.route('/videos/<int:id>')
    def get_video_by_id(id):
        try:
            videos = Video.query.get(id)
            response = videos.format()
        except:
            abort(404)

        return jsonify({
            'success': True,
            'videos': response
        })

    @app.route('/videos/<int:id>', methods=['PATCH'])
    @requires_auth('patch:video')
    def edit_video_by_id(payload, id):
        body = request.json
        video_id = id
        video = Video.query.filter_by(id=video_id).one_or_none()

        if video is None:
            abort(404)

        if 'title' in body:
            video.title = body['title']

        if 'type' in body:
            video.type = body['type']

        try:
            video.insert()

        except Exception:
            abort(400)

        return jsonify({
            'success': True,
            'video': video.format()
        })

    @app.route('/videos/<int:id>', methods=['DELETE'])
    @requires_auth('delete:video')
    def delete_video_by_id(payload, id):
        video_id = id
        video = Video.query.filter_by(id=video_id).one_or_none()

        if not video:
            abort(404)

        try:
            video.delete()
        except:
            abort(400)

        return jsonify({
            'success': True,
            'delete': id
        }), 200

    @app.route("/authorization/url", methods=["GET"])
    def generate_auth_url():
        print(os.environ)
        url = f'https://{AUTH0_DOMAIN}/authorize' \
            f'?audience={API_AUDIENCE}' \
            f'&response_type=token&client_id=' \
            f'{AUTH0_CLIENT_ID}&redirect_uri=' \
            f'{AUTH0_CALLBACK_URL}'
        
        return jsonify({
            'url': url
        })



    # =================================================================
    #  Error Handlers
    # =================================================================

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

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
