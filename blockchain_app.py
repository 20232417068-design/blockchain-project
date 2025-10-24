import hashlib, json, webbrowser, threading
from time import time
from flask import Flask, jsonify, request, render_template, redirect, url_for
from datetime import datetime

# ===================== BLOCKCHAIN CLASS =====================
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(previous_hash='0')

    def create_block(self, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            'transactions': self.transactions,
            'previous_hash': previous_hash,
        }
        block['hash'] = self.hash(block)
        self.transactions = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return self.last_block['index'] + 1

    def reset_chain(self):
        self.chain = []
        self.transactions = []
        self.create_block(previous_hash='0')

    @staticmethod
    def hash(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

# ===================== FLASK APP =====================
app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def home():
    return render_template('index.html', chain=blockchain.chain, total_blocks=len(blockchain.chain))

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    sender = request.form['sender']
    receiver = request.form['receiver']
    amount = request.form['amount']
    blockchain.add_transaction(sender, receiver, float(amount))
    return redirect(url_for('home'))

@app.route('/mine', methods=['POST'])
def mine_block():
    blockchain.create_block(blockchain.last_block['hash'])
    return redirect(url_for('home'))

@app.route('/reset', methods=['POST'])
def reset_blockchain():
    blockchain.reset_chain()
    return redirect(url_for('home'))

@app.route('/chain', methods=['GET'])
def full_chain():
    return jsonify({'chain': blockchain.chain}), 200

# ===================== AUTO OPEN BROWSER =====================
if __name__ == '__main__':
    def open_browser():
        webbrowser.open_new("http://127.0.0.1:5003/")
    threading.Timer(1.5, open_browser).start()
    app.run(host='0.0.0.0', port=5003)
if __name__ == '__main__':
    import os
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
