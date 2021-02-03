from flask import Flask, escape, request, render_template, send_from_directory, url_for, send_file
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
            (invalid_url, dir_name) = IB_obj.start()
            zip_file_name = dir_name + '.zip'
            if not invalid_url:
                print(dir_name)
                return {'status': 'False', 'filename': zip_file_name}
            return {'status': 'True'}
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
            (invalid_url, dir_name) = RG.start(url)
            zip_file_name = os.path.basename(dir_name) + '.zip'
            if not invalid_url:
                print(zip_file_name)
                return {'status': 'False', 'filename': zip_file_name}
            return {'status': 'True'}
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
            (invalid_url, dir_name) = CJ.start(url)
            zip_file_name = os.path.basename(dir_name) + '.zip'
            if not invalid_url:
                print(zip_file_name)
                return {'status': 'False', 'filename': zip_file_name}
            return {'status': 'True'}
            
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
            (invalid_url, dir_name) = BS.start(url)
            zip_file_name = os.path.basename(dir_name) + '.zip'
            if not invalid_url:
                print(zip_file_name)
                return {'status': 'False', 'filename': zip_file_name}
            return {'status': 'True'}
    else:
        error = 'Invalid URL'
    return render_template('BS.html', error=error)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')



@app.route('/download', methods = ['GET', 'POST'])
def download():
    if request.method == 'GET':
        file_path = request.args.get("filepath")
        if file_path is not None:
            #print(f'\n\nFile_path: {file_path}\n\n')
            path = os.path.join(os.getcwd(), file_path)
            #print(f'\n\nFilepath: {path}\n\n')
            return send_file(path, as_attachment=True)
        else:
            return "<p>Error</p>"
    else:
        return "<h3>Internal Error!</h3>"




@app.route('/hello')
def hello(name=None):
    return render_template('homepage.html', name=name)

@app.route('/about')
def about():
    return "<h2>You are at About!</h2>"

if __name__ == '__main__':
    app.run(debug=True)