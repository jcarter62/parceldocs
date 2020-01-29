from flask import Flask, redirect, render_template, request
from appsettings import Settings
from flask_bootstrap import Bootstrap


app = Flask(__name__)
boostrap = Bootstrap(app)

@app.route('/')
def hello_world():
    return redirect('/setup')

@app.route('/setup', methods=['GET', 'POST'])
def route_setup():
    if request.method == 'GET':
        settings = Settings()
        context = {'settings': settings.items}
        return render_template('setup.html', context=context)
    else:
        # Extract each item from form, and save back to settings.
        settings = Settings()
        for item in settings.items:
            formitem = request.form[item['name']]
            item['value'] = formitem
        settings.save_config()
        return redirect('/setup')

if __name__ == '__main__':
    app.run()
