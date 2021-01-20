from flask import Flask, escape, request, render_template, send_from_directory
import IB_scrapper as IB
import os


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    error = None
    if request.method == 'GET':
        url = request.args.get("url")
        if url is not None:
            print(f'\nURL: {url}\n')
            obj = IB.IB(url)
            invalid_url = obj.start()
            #print(f'INVALID URL: {invalid_url}')
            return 'True' if invalid_url else 'False'
    else:
        error = 'Invalid URL'
    return render_template('index.html', error=error)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')


@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/about')
def about():
    return "<h2>You are at About!</h2>"

if __name__ == '__main__':
    app.run(debug=True)