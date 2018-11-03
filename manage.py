from flask import send_file

from apps import create_app


app = create_app('develepment')


@app.route('/')
def index():
    return send_file('./static/index.html')

if __name__ == '__main__':
    # print(app.url_map)
    app.run(port=5021)
