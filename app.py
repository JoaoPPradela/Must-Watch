from flask import Flask, redirect, render_template, request, url_for
from models.database import init_db
from models.lista import Atividade

#Configuração do Flask e Banco de Dados 
app = Flask(__name__)

# Inicia o banco de dados criando a tabela de atividades se necessário
init_db()

# Rota Inicial - Página Home
@app.route('/')
def home():
    return render_template('home.html', titulo='Home')

#Gerenciamento da Lista (Ver e Criar) 
@app.route('/lista', methods=['GET','POST'])
def atividade():
    atividades = None

    # Se receber dados via POST, cria e salva uma nova atividade
    if request.method == 'POST':
        titulo_atividade = request.form['titulo-atividade']
        tipo_de_atividade = request.form['tipo_de_atividade']
        indicado_por = request.form['indicado_por']
    
        atividade = Atividade(titulo_atividade, tipo_de_atividade, indicado_por)
        atividade.salvar_atividade()

    # Busca todas as atividades cadastradas para exibir na página
    atividades = Atividade.obter_atividades()
    return render_template('lista.html', titulo='Sua Lista de Desejos', atividades=atividades)

# Rota para Excluir uma atividade existente
@app.route('/delete/<int:idAtividade>')
def delete(idAtividade):
    """ Localiza a atividade pelo ID e a remove do banco """
    atividade = Atividade.id(idAtividade)
    atividade.excluir_atividade()
    return redirect(url_for('atividade'))

# Rota para Editar uma atividade existente
@app.route('/update/<int:idAtividade>', methods=['GET', 'POST']) 
def update(idAtividade):
    atividades = None

    #Se o formulário de edição for enviado, atualiza os dados existentes
    if request.method == 'POST':
        titulo_atividade = request.form['titulo-atividade']
        tipo_de_atividade = request.form['tipo_de_atividade']
        # Cria o objeto com o ID existente para saber qual linha atualizar
        atividade = Atividade(titulo_atividade, tipo_de_atividade, id_atividade=idAtividade)
        atividade.atualizar_atividade()

    # Recarrega a lista completa e a atividade específica para preencher o form de edição
    atividades = Atividade.obter_atividades()
    atividade_selecionada = Atividade.id(idAtividade)
    return render_template('lista.html', titulo=f'Editando a atividade ID: {idAtividade}', atividade_selecionada=atividade_selecionada, atividades=atividades)

# Rota de Teste
@app.route('/ola')
def ola_mundo():
    return "Olá, Mundo!"