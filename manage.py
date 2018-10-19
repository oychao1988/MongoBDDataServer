from apps import create_app


app = create_app('develepment')


if __name__ == '__main__':
    app.run(port=5021)
