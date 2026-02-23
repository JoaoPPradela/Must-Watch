
from flask import Flask, redirect, render_template, request, url_for
from models.database import init_db
from models.lista import Atividade

app = Flask(__name__)

init_db()

@app.route('/')
def home():
    return render_template('home.html', titulo='Home')

@app.route('/lista', methods=['GET','POST'])
def atividade():
    atividades = None

    if request.method == 'POST':
        titulo_atividade = request.form['titulo-atividade']
        tipo_de_atividade = request.form['tipo_de_atividade']
        indicado_por = request.form['indicado_por']
    
        atividade = Atividade(titulo_atividade, tipo_de_atividade,indicado_por)
        atividade.salvar_atividade()

    atividades = Atividade.obter_atividades()
    return render_template('lista.html', titulo='Sua Lista de Desejos', atividades=atividades)

@app.route('/delete/<int:idAtividade>')
def delete(idAtividade):
    atividade = Atividade.id(idAtividade)
    atividade.excluir_atividade()
    # return render_template('agenda.html', titulo="Agenda",
    # tarefa=tarefas)
    return redirect(url_for('atividade'))

@app.route('/update/<int:idAtividade>', methods=['GET', 'POST']) 
def update(idAtividade):
    atividades = None

    if request.method == 'POST':
        titulo_atividade = request.form['titulo-atividade']
        tipo_de_atividade = request.form['tipo_de_atividade']
        atividade = Atividade(titulo_atividade, tipo_de_atividade, idAtividade)
        atividade.atualizar_atividade()

    atividades = Atividade.obter_atividades()
    atividade_selecionada = Atividade.id(idAtividade)
    return render_template('lista.html', titulo=f'Editando a atividade ID: {idAtividade}',atividade_selecionada=atividade_selecionada, atividades=atividades)

@app.route('/ola')
def ola_mundo():
    return "Olá, Mundo!"