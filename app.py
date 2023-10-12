import json
from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd

app = Flask(__name__) 
cors = CORS(app, resources={r"/": {"origins": "*.*"}})

def extract():
    return pd.read_csv('historico.csv',delimiter=';', encoding='utf-8')

def transform():
    historico = extract()
    historico['mes'] = historico['data'].apply(lambda x: str(x).split('/')[1])
    historico['ano'] = historico['data'].apply(lambda x: str(x).split('/')[2])
    historico['saldo'] = historico['valor'].apply(lambda x: float(str(x).replace(',','.')))
    historico['saldo'] = historico['saldo']*historico['quantidade']
    return historico.groupby(by=['mes','ano','nome']).apply(lambda x: x.to_json(orient='records')).values

@app.route("/", methods=['GET']) 
@cross_origin()
def home(): 
    return jsonify({
        "api": "API",
        "description":"ETL (Extract, transform, load) para csv com lista de produtos",
        "version": "1.0.1"
    })
    
@app.route("/api/<name>", methods=['GET']) 
@cross_origin()
def load(name):
    res = 'Vazio'
    if name == 'true':
        res = [json.loads(x)[0] for x in transform()]
        print(res)
    return render_template("index.html", res=res)

if __name__ == '__main__':
    app.run(debug=False, port=5000)