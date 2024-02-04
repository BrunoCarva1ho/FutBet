from flask import Flask, render_template, redirect, request, flash
import requests
import json

#Link do banco Firebase
link = "https://futbet-198b9-default-rtdb.firebaseio.com/"


app = Flask(__name__)
app.config['SECRET_KEY']= ['tony']


@app.route('/')
def index():
    return render_template("inicio.html")


@app.route('/registro.html', methods=['POST','GET'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        
        dados = {
            'usuario': usuario,
            'senha': senha
        }
        
        requests.post(f'{link}/usuarios/.json', data= json.dumps(dados))
        
        return redirect('/login.html')
    
    return render_template("registro.html")


@app.route('/login.html', methods=['POST', 'GET'])
def login():
    
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuarios = requests.get(f'{link}/usuarios/.json').json()
        
        for user in usuarios:
            print(usuarios[user]['usuario'])
            if(usuarios[user]['usuario'] == email and usuarios[user]['senha'] == senha):
                
                tuplas = []
                palpites = requests.get(f'{link}/palpites/.json').json()
    
                for p in palpites:
                    tupla = (palpites[p]['usuario'], palpites[p]['palpite'], palpites[p]['likes'], palpites[p]['deslikes'])
                    tuplas.append(tupla)
                    
                return render_template("principal.html", id=usuarios[user]['usuario'], palpites=tuplas)
        

    return render_template("login.html")


@app.route('/principal.html/<id>')
def principal(id):
    
    tuplas = []
    palpites = requests.get(f'{link}/palpites/.json').json()
    
    for p in palpites:
        tupla = (palpites[p]['usuario'], palpites[p]['palpite'], palpites[p]['likes'], palpites[p]['deslikes'])
        tuplas.append(tupla)
    
    return render_template("principal.html", palpites=tuplas, id=id)


@app.route('/palpite.html/<id>', methods=['POST', 'GET'])
def palpite(id):
    
    if request.method =='POST':
        
        palpite = request.form['palpite']
        
        dados = {
            'usuario': id,
            'palpite': palpite,
            'likes': 0,
            'deslikes': 0
        }
        
        requests.post(f'{link}/palpites/.json', data= json.dumps(dados))
        
        return redirect(f'/principal.html/{id}')
        
    return render_template("palpite.html", id=id)


@app.route('/like/<usuario>/<palpite>/<id>')
def likes(usuario, palpite, id):
    
    palpites = requests.get(f'{link}/palpites/.json').json()
    
    for p in palpites:
        if(palpites[p]['palpite'] == palpite and palpites[p]['usuario'] == usuario):
            idUsuario = p
            atual = palpites[p]['likes']        
    
    dados = {
        'likes': atual+1
    }
    
    requests.patch(f'{link}/palpites/{idUsuario}/.json', data= json.dumps(dados))
    
    return redirect(f'/principal.html/{id}')

    
@app.route('/deslike/<usuario>/<palpite>/<id>')
def deslike(usuario, palpite, id):
    
    palpites = requests.get(f'{link}/palpites/.json').json()
    
    for p in palpites:
        if(palpites[p]['palpite'] == palpite and palpites[p]['usuario'] == usuario):
            idUsuario = p
            atual = palpites[p]['deslikes']        
    
    dados = {
        'deslikes': atual+1
    }
    
    requests.patch(f'{link}/palpites/{idUsuario}/.json', data= json.dumps(dados))
    
    return redirect(f'/principal.html/{id}')


if __name__ == '__main__':
    app.run(debug=True)