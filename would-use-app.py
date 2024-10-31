from flask import Flask, jsonify, request, render_template 
from pydantic import ValidationError
import joblib
import pandas as pd
from pydantic import BaseModel
from flask_cors import CORS
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
conexao = MongoClient(os.getenv("DB_MONGO_URL"))
db_name = conexao[os.getenv("DB_MONGO_NAME")]
collection_ia = db_name[os.getenv("DB_MONGO_COLLECTION_IA")] 

# DTO
class WouldUseAppInputDTO(BaseModel):
    comunidade: str  # Participante da Comunidade LGBTQIA+
    faixa_etaria: str  # Faixa Etária
    identidade_genero: str  # Identidade de Gênero
    orientacao_sexual: str  # Orientação Sexual
    cidade_estado: str  # Cidade/Estado
    escolaridade: str  # Escolaridade
    usa_apps_emprego: str  # Usa Apps para Oportunidades de Emprego?
    preferencia_cursos: str  # Preferência de Cursos
    desafios_emprego_genero: str  # Desafios de Emprego por Gênero
    interesse_empreender: str  # Interesse em Empreender
    situacao_mercado_trabalho: str  # Situação no Mercado de Trabalho
    usa_redes_sociais: str  # Usa Redes Sociais?

# Inicializando o app Flask
app = Flask(__name__)

CORS(app)

# Rota POST para enviar dados do user
@app.route('/would-use-app', methods=['POST'])
def post_would_use_app():
    try:
        # Obtém os dados enviados no corpo da requisição (formato JSON)
        data = request.get_json()

        # Valida e transforma os dados com o DTO
        user = WouldUseAppInputDTO(**data)

        # Verifica se o usuário não faz parte da comunidade
        if user.comunidade.lower() == 'não':
            response = {
                'message': 'Dados recebidos e válidos!',
                'data': user.dict(),  # Converte o objeto Pydantic em um dicionário
                'prediction': "Não usaria o app" 
            }

            #Salvando no banco
            collection_ia.insert_one({"user": user.dict(), "prediction": "Não usaria o app" })

            # Renderiza a resposta na página de resultados
            return render_template('respostas.html', message=response['message'], data=response['data'], prediction=response['prediction'])


        # Cria um DataFrame com os dados do user
        new_row_df = pd.DataFrame([user.dict().values()], columns=[
            "Participante da Comunidade LGBTQIA+", 
            "Faixa Etária", 
            "Identidade de Gênero", 
            "Orientação Sexual", 
            "Cidade/Estado", 
            "Escolaridade", 
            "Usa Apps para Oportunidades de Emprego?", 
            "Preferência de Cursos", 
            "Desafios de Emprego por Gênero", 
            "Interesse em Empreender", 
            "Situação no Mercado de Trabalho", 
            "Usa Redes Sociais?"
        ])
        
        # Corrigindo valores na coluna 'Identidade de Gênero'
        new_row_df['Identidade de Gênero'] = new_row_df['Identidade de Gênero'].replace({
            "Geladeira Eletrolux de duas portas com gelo para água ": "Outra",
            "Mulher transgênero": "transgênero",
            "Homem transgênero": "transgênero"
        })

        # Corrigindo valores na coluna 'Escolaridade'
        new_row_df['Escolaridade'] = new_row_df['Escolaridade'].replace({
            "Ensino Médio completo": "Ensino Médio completo ou cursando",
            "Ensino Superior completo": "Ensino Superior completo ou cursando",  
            "Ensino Superior completo ou cursando\xa0": "Ensino Superior completo ou cursando",  
            "Ensino Médio completo": "Ensino Médio completo ou cursando",
            "Ensino Fundamental completo": "Ensino Fundamental completo ou cursando"
        })

        # Corrigindo valores na coluna 'Preferência de Cursos'
        new_row_df['Preferência de Cursos'] = new_row_df['Preferência de Cursos'].replace({
            "Não tenho preferência, pode ser online ou presencial": "Não tenho preferência, pode ser on-line ou presencial",
            "Prefiro cursos online": "Prefiro cursos on-line"
        })

        # Corrigindo valores na coluna 'Situação no Mercado de Trabalho'
        new_row_df['Situação no Mercado de Trabalho'] = new_row_df['Situação no Mercado de Trabalho'].replace({
               "  Desempregado (a)": "Desempregado (a)",
                "Autônomo (a)": "Desempregado (a)",
                "  Empregado (a)": "Empregado (a)",
        })

        # Carregando o modelo
        pipeline_carregado = joblib.load('modelo_pipeline.pkl')
        previsao = pipeline_carregado.predict(new_row_df)

        prediction = "Usuaria o app" if previsao[0] == "Usario o app" else "Não usaria o app" 

        # Prepara a resposta baseada nos dados validados e na previsão
        response = {
            'message': 'Dados recebidos e válidos!',
            'data': user.dict(),  # Converte o objeto Pydantic em um dicionário
            'prediction': prediction
        }

        #Salvando no banco
        collection_ia.insert_one({"user": user.dict(), "prediction": prediction })

        # Renderiza a resposta na página de resultados
        return render_template('respostas.html', message=response['message'], data=response['data'], prediction=response['prediction'])

    except ValidationError as e:
        # Se os dados forem inválidos, retornamos um erro
        return jsonify({'error': 'Dados inválidos!', 'details': e.errors()}), 400
    
@app.route('/', methods=['GET'])
def pagina_inicial():
    return render_template('index.html')

@app.route('/forms')
def forms():
    return render_template('forms.html')  # Renderiza o forms.html que deve estar na pasta templates


# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True, port=5980)
