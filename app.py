from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Permitir requisições do frontend

# Configuração do banco de dados
DATABASE = 'participantes.db'

def init_db():
    """Inicializa o banco de dados"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            empresa TEXT,
            cargo TEXT,
            aceite BOOLEAN NOT NULL,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resultado_roleta TEXT,
            data_resultado TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

def save_participante(data):
    """Salva os dados do participante no banco"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO participantes (nome, telefone, empresa, cargo, aceite, data_cadastro)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['nome'],
            data['telefone'],
            data['empresa'],
            data['cargo'],
            data['aceite'],
            datetime.now().isoformat()
        ))
        
        participante_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"Participante salvo com ID: {participante_id}")
        return {'success': True, 'id': participante_id}
        
    except Exception as e:
        conn.close()
        print(f"Erro ao salvar participante: {e}")
        return {'success': False, 'error': str(e)}

def update_resultado(participante_id, resultado):
    """Atualiza o resultado da roleta"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE participantes 
            SET resultado_roleta = ?, data_resultado = ?
            WHERE id = ?
        ''', (resultado, datetime.now().isoformat(), participante_id))
        
        conn.commit()
        conn.close()
        
        print(f"Resultado atualizado para participante ID: {participante_id}")
        return {'success': True}
        
    except Exception as e:
        conn.close()
        print(f"Erro ao atualizar resultado: {e}")
        return {'success': False, 'error': str(e)}

@app.route('/')
def index():
    """Serve o arquivo HTML"""
    return send_from_directory('.', 'roleta.html')

@app.route('/api/salvar-participante', methods=['POST'])
def salvar_participante():
    """Endpoint para salvar dados do participante"""
    try:
        data = request.get_json()
        
        # Validações básicas
        if not data.get('nome') or len(data['nome'].strip()) < 3:
            return jsonify({'success': False, 'error': 'Nome inválido'}), 400
            
        if not data.get('telefone'):
            return jsonify({'success': False, 'error': 'Telefone obrigatório'}), 400
            
        if not data.get('aceite'):
            return jsonify({'success': False, 'error': 'Aceite obrigatório'}), 400
        
        # Salvar no banco
        result = save_participante(data)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        print(f"Erro no endpoint: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@app.route('/api/atualizar-resultado', methods=['POST'])
def atualizar_resultado():
    """Endpoint para atualizar resultado da roleta"""
    try:
        data = request.get_json()
        
        if not data.get('participante_id') or not data.get('resultado'):
            return jsonify({'success': False, 'error': 'Dados incompletos'}), 400
        
        result = update_resultado(data['participante_id'], data['resultado'])
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        print(f"Erro no endpoint: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@app.route('/api/participantes', methods=['GET'])
def listar_participantes():
    """Endpoint para listar todos os participantes"""
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nome, telefone, empresa, cargo, aceite, data_cadastro, resultado_roleta, data_resultado
            FROM participantes
            ORDER BY data_cadastro DESC
        ''')
        
        participantes = []
        for row in cursor.fetchall():
            participantes.append({
                'id': row[0],
                'nome': row[1],
                'telefone': row[2],
                'empresa': row[3],
                'cargo': row[4],
                'aceite': bool(row[5]),
                'data_cadastro': row[6],
                'resultado_roleta': row[7],
                'data_resultado': row[8]
            })
        
        conn.close()
        return jsonify({'success': True, 'participantes': participantes}), 200
        
    except Exception as e:
        print(f"Erro ao listar participantes: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    # Inicializar banco de dados
    init_db()
    
    # Configuração para produção
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("🚀 Servidor iniciado!")
    print("📊 Banco de dados: participantes.db")
    print(f"🌐 Acesse: http://localhost:{port}")
    print("📋 API Endpoints:")
    print("   POST /api/salvar-participante")
    print("   POST /api/atualizar-resultado")
    print("   GET  /api/participantes")
    
    app.run(debug=debug, host='0.0.0.0', port=port) 