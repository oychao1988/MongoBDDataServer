from flask import jsonify

from apps import create_app


app = create_app('develepment')


@app.route('/')
def index():
    API = {
        '/recruits': {
            '/duplicateChecking': {'GET': {'params':['number', 'updateDate', 'source']},
                                   'POST': {'params':['number', 'updateDate', 'source']},
                                   'PUT': {'params':['number', 'updateDate', 'source']},
                                   'DELETE': {'params':['number']},
            },
            '/lagou': {'GET': {'params':[]},
                       'POST': {'params':[]},
                       'PUT': {'params':[]},
                       'DELETE': {'params':[]},
            },
            '/zhilian': {'GET': {'params': []},
                       'POST': {'params': []},
                       'PUT': {'params': []},
                       'DELETE': {'params': []},
                       },
            '/51job': {'GET': {'params': []},
                       'POST': {'params': []},
                       'PUT': {'params': []},
                       'DELETE': {'params': []},
                       },
            '/liepin': {'GET': {'params': []},
                       'POST': {'params': []},
                       'PUT': {'params': []},
                       'DELETE': {'params': []},
                       },
            '/zhipin': {'GET': {'params': []},
                       'POST': {'params': []},
                       'PUT': {'params': []},
                       'DELETE': {'params': []},
                       },
        }
    }
    return jsonify(API)

if __name__ == '__main__':
    # print(app.url_map)
    app.run(port=5021)
