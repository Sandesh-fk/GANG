from flask import Flask, request, jsonify, send_from_directory
from geo_analysis import get_de_genes
import os

app = Flask(__name__, static_folder='../frontend', static_url_path='')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/de_genes')
def de_genes():
    geo = request.args.get('geo')
    col = request.args.get('group_col')
    g1 = request.args.get('group1')
    g2 = request.args.get('group2')
    top_n = int(request.args.get('top_n', 20))
    try:
        results = get_de_genes(geo, col, g1, g2, top_n)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
