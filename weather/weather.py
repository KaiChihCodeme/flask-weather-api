from flask import Blueprint, abort, json, jsonify, request
from db import db_add_weather, db_get_all_weathers, db_get_all_weathers_paging, db_get_weather, db_update_weather, db_delete_weather
from exceptions import KeyNotExistException
from cache import redis
from flask import current_app as app

weather_bp = Blueprint('weather', __name__, url_prefix='/weather')

@weather_bp.route('/', methods=['POST'])
def create_weather():
    """
    Create weather
    ---
    tags:
        - weather
    produces:
        - application/json  
    parameters:
        - name: body
          in: body
          schema:
            id: weather
            required:
                - city
                - temperature
                - humidity
                - description
            properties:
                city:
                    type: string
                    description: weather of city
                temperature:
                    type: number
                    format: float
                    description: weather temperature
                humidity:
                    type: number
                    format: float
                    description: weather humidity
                description:
                    type: string
                    description: weather description
    responses:
        200:
            description: weather successfully created
            schema:
                id: weathers
                properties:
                    message:
                        type: string
                    weather:
                        $ref: '#/definitions/weather'
        400:
            description: weather creation failed
            schema:
                id: weathers
                properties:
                    message:
                        type: string
                    required:
                        type: array
                        items:
                            type: string
    """
    missing_params = validate_required_creation_params(request.json)
    if missing_params:
        resp = validation_failed_resp(missing_params)
        return jsonify(resp), 200

    weather = db_add_weather(request.json['city'], request.json['temperature'], request.json['humidity'], request.json['description'])
    resp = create_response("weather successfully created!", weather)
    
    # delete cache to refresh
    redis.delete('all_weathers')
    
    return jsonify(resp), 200

@weather_bp.route('/', methods=['GET'])
def get_all_weathers():
    """
    Get All weathers
    ---
    tags:
        - weather
    produces:
        - application/json
    responses:
        200:
            description: All weathers
            schema:
                id: weathers
                properties:
                    weathers:
                        type: array
                        items:
                            $ref: '#/definitions/weather'
    """
    
    # Get cache at first
    cached_weathers = redis.get('all_weathers')
    if cached_weathers:
        app.logger.info("Hit cache in getting all weathers")
        weathers_result = json.loads(cached_weathers)
    else:
        app.logger.info("Miss cache in getting all weathers")
        weathers = db_get_all_weathers()
        weathers_result = [weather.to_dict() for weather in weathers]
        redis.set('all_weathers', json.dumps(weathers_result))
    
    resp = {
        'weathers': weathers_result
    }
    return jsonify(resp), 200

@weather_bp.route('/<int:page>/<int:limit>', methods=['GET'])
def get_all_weathers_by_paging(page, limit):
    """
    Get All weathers by Paging
    For boosting performance, we can limit the number of weathers to be displayed in a single page.
    ---
    tags:
        - weather
    produces:
        - application/json
    parameters:
        - name: page
          in: path
          type: integer
          required: true
          description: Page number
        - name: limit
          in: path
          type: integer
          required: true
          description: Number of weathers per page
    responses:
        200:
            description: All weathers with paging
            schema:
                id: weathers
                properties:
                    weathers:
                        type: array
                        items:
                            $ref: '#/definitions/weather'
                    total:
                        type: integer
                    pages:
                        type: integer
                    page:
                        type: integer
    """
    paginated_weathers = db_get_all_weathers_paging(page, limit)
    weathers = [weathers.to_dict() for weathers in paginated_weathers.items]
    resp = {
        'weathers': weathers,
        'total': paginated_weathers.total,
        'pages': paginated_weathers.pages,
        'page': page
    }
    return jsonify(resp), 200

@weather_bp.route('/<int:id>', methods=['GET'])
def get_weather(id):
    """
    Get weather by Id
    ---
    tags:
        - weather
    produces:
        - application/json
    parameters:
        - name: id
          in: path
          type: integer
          required: true
          description: weather id
    responses:
        200:
            description: weather details
            schema:
                id: weather
                properties:
                    weather:
                        $ref: '#/definitions/weather'
        404:
            description: weather not found
            schema:
                id: weather
                properties:
                    message:
                        type: string
    """
    weather = db_get_weather(id)
    if weather:
        resp = create_response("weather details by id", weather)
        return jsonify(resp), 200
    
    # if not found
    return jsonify({'message': f'No weather Found in id: {id}'}), 404

@weather_bp.route('/<int:id>', methods=['PATCH'])
def update_weather(id):
    """
    Updatge weather by ID
    ---
    
    tags:
        - weather
    produces:
        - application/json
    parameters:
        - name: id
          in: path
          type: integer
          required: true
          description: weather id
        - name: body
          in: body
          required: true
          schema:
            id: weather
            properties:
                city:
                    type: string
                    description: weather city
                temperature:
                    type: number
                    format: float 
                    description: weather temperature
                humidity:
                    type: number
                    format: float
                    description: weather humidity
                description:
                    type: string
                    description: weather description
    responses:
        200:
            description: weather successfully updated
            schema:
                id: weather
                properties:
                    message:
                        type: string
                    weather:
                        $ref: '#/definitions/weather'
        400:
            description: Invalid key
            schema:
                id: weather
                properties:
                    message:
                        type: string
        404:
            description: weather not found
            schema:
                id: weather
                properties:
                    message:
                        type: string
        500:
            description: Something went wrong
            schema:
                id: weather
                properties:
                    message:
                        type: string
    """
    updated_weather = db_update_weather(id, **request.json)
    if isinstance(updated_weather, KeyNotExistException):
        app.logger.debug(f"Invalid key in updating weather: {updated_weather.key}")
        return jsonify({'message': updated_weather.message}), 400
    if isinstance(updated_weather, Exception):
        app.logger.error(f"Error in updating weather: {updated_weather}")
        return jsonify({'message': 'Something went wrong!'}), 500
    if updated_weather:
        resp = create_response("weather successfully updated!", updated_weather)
        
        # delete cache to refresh
        redis.delete('all_weathers')
        
        return jsonify(resp), 200
    
    return jsonify({'message': f'weather id: {id} not found!'}), 404

@weather_bp.route('/<int:id>', methods=['DELETE'])
def delete_weather(id):
    """
    Delete weather by ID
    ---
    tags:
        - weather
    produces:
        - application/json
    parameters:
        - name: id
          in: path
          type: integer
          required: true
          description: weather id
    responses:
        200:
            description: weather successfully removed
            schema:
                id: weather
                properties:
                    message:
                        type: string
        404:
            description: weather not found
            schema:
                id: weather
                properties:
                    message:
                        type: string
    """
    deleted = db_delete_weather(id)
    if deleted:
        resp = {
            'message': 'weather successfully removed!'
        }
        
        # delete cache to refresh
        redis.delete('all_weathers')
        
        return jsonify(resp), 200
    resp = {
        'message': 'No weather Found'
    }
    return jsonify(resp), 404

# create general response for weather
def create_response(message, weathers):
    if not isinstance(weathers, list):
        weathers = [weathers]
        
    weathers_dict = [weather.to_dict() for weather in weathers]
    
    response = {
        'message': message,
        'weather': weathers_dict
    }
    
    return response

def validate_required_creation_params(params):
    required_params = ['city', 'temperature', 'humidity', 'description']
    missing_params = [param for param in required_params if param not in params]
    return missing_params

# verify creation parameters
def validation_failed_resp(params):
    response = {
        'message': 'weather creation failed!',
        'required': params
    }
    return response