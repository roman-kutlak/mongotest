import os
import flask

app = flask.Flask('stitch_main')


@app.route('/')
def index():
    return flask.render_template('stitch_main/index.html', service_name=os.environ['SERVICE_NAME'])


def main():
    app.run()


if __name__ == '__main__':
    main()
