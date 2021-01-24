from flask import Flask, escape, request, render_template, send_from_directory, url_for
import IB_scrapper as IB
import os
import RG_scrapper as RG
import CJ_scrapper as CJ
import BS_scrapper as BS


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/IB', methods=['GET', 'POST'])
def Idlebrain():
    error = None
    if request.method == 'GET':
        url = request.args.get("url")
        if url is not None:
            print(f'\nURL: {url}\n')
            IB_obj = IB.IB(url)
            invalid_url = IB_obj.start()
            #print(f'INVALID URL: {invalid_url}')
            return 'True' if invalid_url else 'False'
    else:
        error = 'Invalid URL'
    return render_template('IB.html', error=error)


@app.route('/RG', methods=['GET', 'POST'])
def ragalahari():
    error = None
    if request.method == 'GET':
        url = request.args.get("url")
        if url is not None:
            print(f'\nURL: {url}\n')
            invalid_url = RG.start(url)
            return 'True' if invalid_url else 'False'
    else:
        error = 'Invalid URL'
    return render_template('RG.html', error=error)


@app.route('/CJ', methods=['GET', 'POST'])
def cinejosh():
    error = None
    if request.method == 'GET':
        url = request.args.get("url")
        if url is not None:
            print(f'\nURL: {url}\n')
            invalid_url = CJ.start(url)
            return 'True' if invalid_url else 'False'
    else:
        error = 'Invalid URL'
    return render_template('CJ.html', error=error)


@app.route('/BS', methods=['GET', 'POST'])
def bst():
    error = None
    if request.method == 'GET':
        url = request.args.get("url")
        if url is not None:
            print(f'\nURL: {url}\n')
            invalid_url = BS.start(url)
            return 'True' if invalid_url else 'False'
    else:
        error = 'Invalid URL'
    return render_template('BS.html', error=error)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')


@app.route('/hello')
def hello(name=None):
    return render_template('homepage.html', name=name)

@app.route('/about')
def about():
    return "<h2>You are at About!</h2>"

if __name__ == '__main__':
    app.run(debug=True)