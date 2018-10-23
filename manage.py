from flask import jsonify

from apps import create_app


app = create_app('develepment')


@app.route('/')
def index():
    API = {
        '/recruit': {
            '/duplicateChecking': {'GET': {'params':['number', 'updateDate', 'source']},
                                   'POST': {'params':['number', 'updateDate', 'source']},
                                   'PUT': {'params':['number', 'updateDate', 'source']},
                                   'DELETE': {'params':['number']},
            },
            '/lagou': {'GET': {'params':[]},
                       'POST': {'params':[]},
                       'PUT': {'params':[]},
                       'DELETE': {'params':[]},
            }
        }
    }
    return jsonify(API)

if __name__ == '__main__':
    # print(app.url_map)
    app.run(port=5021)
