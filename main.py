from flask import Flask, render_template, redirect, request, flash
import json
import ast 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rodrigos'

logado = False


@app.route('/')
def home():

    global logado 
    logado = False
    return render_template('login.html')

@app.route('/adm')
def adm():
    if logado == True:
        with open ('usuario.json') as usuariosTemp:
            usuarios = json.load(usuariosTemp)
        
        return render_template ('administrador.html', usuarios=usuarios)
    if logado == False:
       return redirect('/') 

@app.route('/login', methods=['POST'])
def login():

    global logado
     
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    with open ('usuario.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)
        cont = 0

        for usuario in usuarios:
            cont += 1
            if nome == 'admin' and senha == 'Rod1999@': #Dentro da herança, o admin é o administrador (criador de todas as contas) e o restante criado é o usuario normal.
                logado = True
                return redirect('/adm') 
            
            if usuario ['nome'] == nome and usuario ['senha'] == senha:#O usuario normal, só pode ter acesso ao trabalho e nada mais.
                return render_template('usuario.html')
            
            if cont >= len(usuarios):
                flash('USUÁRIO INVÁLIDO!')
                return redirect('/')
            
@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():

    global logado
    user = []
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    user = [
            {
                "nome": nome,
                "senha": senha 
            }
    ]

    with open ('usuario.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)

    usuarioNovo = usuarios + user

    with open ('usuario.json', 'w') as gravarTemp:
        json.dump(usuarioNovo, gravarTemp, indent=4)
    logado = True
    flash(F'Parabéns {nome}, você foi cadastrado!!')

    return redirect('/adm')

@app.route('/excluirUsuario', methods =['POST'])
def excluirUsuario():
    global logado
    logado = True
    usuario = request.form.get('usuariosPexcluir')
    usuarioDict = ast.literal_eval(usuario)
    nome = usuarioDict['nome']
    with open('usuario.json') as usuariosTemp:
        usuariosJson = json.load(usuariosTemp)
        for c in usuariosJson:
            if c == usuarioDict:
                usuariosJson.remove(usuarioDict)
                with open('usuario.json', 'w') as usuarioAexcluir:
                    json.dump(usuariosJson, usuarioAexcluir, indent=4)

    flash(F'Conluído! {nome} foi excluído!')
    return redirect('/adm')



if __name__ == "__main__":
    app.run(debug=True)    