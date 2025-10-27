# -------------------------------------------------------------
#  Blockchain Transaction Web App (Dark Theme + Theme Toggle + Blue Chain Icon)
# -------------------------------------------------------------

from flask import Flask, request, render_template_string
import hashlib, json
from datetime import datetime

# -------------------- Blockchain Logic --------------------

class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = str(datetime.now())
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    difficulty = 3  # Mining difficulty

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, [], "0")
        self.chain.append(genesis)

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, name, number, amount):
        now = datetime.now()
        transaction = {
            "name": name,
            "transaction_number": number,
            "amount": amount,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S")
        }
        self.pending_transactions.append(transaction)

    def proof_of_work(self, block):
        block.nonce = 0
        hash_value = block.compute_hash()
        while not hash_value.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            hash_value = block.compute_hash()
        return hash_value

    def mine_block(self):
        if not self.pending_transactions:
            return None

        last_block = self.get_last_block()
        new_block = Block(last_block.index + 1, self.pending_transactions, last_block.hash)
        new_block.hash = self.proof_of_work(new_block)

        self.chain.append(new_block)
        self.pending_transactions = []

        return new_block

    def reset_chain(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()


# -------------------- Flask Web App --------------------

app = Flask(__name__)
blockchain = Blockchain()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>🔗 Blockchain Transaction Web App</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">

    <style>
        body { background: #0d1117; color: #e6e6e6; font-family: 'Segoe UI', sans-serif; }
        .navbar { background: #161b22 !important; border-bottom: 1px solid #30363d; }
        .navbar-brand { font-weight: bold; font-size: 26px; color: #58a6ff !important; }
        .container { margin-top: 35px; max-width: 1150px; }

        .block-card {
            background: #161b22;
            padding: 18px;
            border-radius: 12px;
            margin-bottom: 18px;
            border-left: 6px solid #58a6ff;
            box-shadow: 0px 2px 8px rgba(255,255,255,0.05);
        }

        .form-control { background: #21262d; border: 1px solid #30363d; color: white; }
        .form-control:focus { border-color: #58a6ff; }

        .btn { border-radius: 8px; font-weight: 600; }
        .btn-primary { background: #238636; border: none; }
        .btn-primary:hover { background: #2ea043; }
        .btn-danger { background: #d63b3b; border: none; }
        .btn-danger:hover { background: #ff4d4d; }

        .alert-info { background: #161b22; border: 1px solid #30363d; color: #58a6ff; }
        h3, h5, strong { color: #58a6ff; }

        /* LIGHT THEME */
        .light-theme { background: #f4f7fb !important; color: #000 !important; }
        .light-theme .navbar { background: #ffffff !important; border-bottom-color: #dcdcdc !important; }
        .light-theme .navbar-brand { color: #0056b3 !important; }
        .light-theme .block-card { background: #ffffff !important; border-left-color: #0056b3 !important; color: black !important; }
        .light-theme .form-control { background: white !important; border-color: #c8c8c8 !important; color: black !important; }
        .light-theme .alert-info { background: #d9ecff !important; color: #003f75 !important; }
    </style>
</head>
<body>

<nav class="navbar shadow-sm px-4 py-3 d-flex justify-content-between align-items-center">
    <span class="navbar-brand">
      <img src="https://cdn-icons-png.flaticon.com/512/1006/1006771.png" width="35" style="margin-right:6px; filter: hue-rotate(200deg);"> 

        Blockchain Transaction Web App
    </span>

    <button id="themeToggle" class="btn btn-outline-light">🌙 Dark Mode</button>
</nav>

<div class="container">

    <form action="/add_transaction" method="post" class="row g-2 mb-4">
        <div class="col-md-3"><input name="name" class="form-control" placeholder="Name" required></div>
        <div class="col-md-3"><input name="number" class="form-control" placeholder="Transaction No." required></div>
        <div class="col-md-3"><input type="number" name="amount" class="form-control" placeholder="Amount (₹)" required></div>
        <div class="col-md-3"><button class="btn btn-primary w-100">Add Transaction</button></div>
    </form>

    <form action="/mine" method="post" class="d-inline">
        <button class="btn btn-primary mb-3">⛏ Mine Block</button>
    </form>

    <form action="/delete" method="post" class="d-inline">
        <button class="btn btn-danger mb-3">🗑 Reset Blockchain</button>
    </form>

    <div class="alert alert-info mt-3"><strong>Total Blocks:</strong> {{ chain|length }}</div>

    <h3 class="mt-4">Blockchain Ledger:</h3>

    {% for block in chain %}
    <div class="block-card">
        <h5><strong>Block #{{ block.index }}</strong></h5>
        <p><strong>Timestamp:</strong> {{ block.timestamp }}</p>
        <p><strong>Previous Hash:</strong> {{ block.previous_hash }}</p>
        <p><strong>Hash:</strong> {{ block.hash }}</p>
        <p><strong>Nonce:</strong> {{ block.nonce }}</p>
        <h6><strong>Transactions:</strong></h6>

        {% if block.transactions %}
        <ul>
            {% for tx in block.transactions %}
            <li>{{ tx["name"] }} | {{ tx["transaction_number"] }} | ₹{{ tx["amount"] }} | {{ tx["date"] }} {{ tx["time"] }}</li>
            {% endfor %}
        </ul>
        {% else %}
        <p>No transactions in this block.</p>
        {% endif %}
    </div>
    {% endfor %}

</div>

<script>
const toggleBtn = document.getElementById("themeToggle");
const body = document.body;

if(localStorage.getItem("theme") === "light"){
    body.classList.add("light-theme");
    toggleBtn.innerHTML = "☀️ Light Mode";
}

toggleBtn.addEventListener("click", () => {
    body.classList.toggle("light-theme");

    if(body.classList.contains("light-theme")){
        toggleBtn.innerHTML = "☀️ Light Mode";
        localStorage.setItem("theme","light");
    } else {
        toggleBtn.innerHTML = "🌙 Dark Mode";
        localStorage.setItem("theme","dark");
    }
});
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE, chain=blockchain.chain)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    blockchain.add_transaction(request.form['name'], request.form['number'], request.form['amount'])
    return index()

@app.route('/mine', methods=['POST'])
def mine():
    blockchain.mine_block()
    return index()

@app.route('/delete', methods=['POST'])
def delete():
    blockchain.reset_chain()
    return index()



if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
