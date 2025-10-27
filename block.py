# -------------------------------------------------------------
#  Blockchain Application (Enhanced Version)
#  Author: Your Name
#  Description: A simple blockchain storing transactions
#  with transaction numbers, timestamps, and reset options.
# -------------------------------------------------------------

import hashlib
import json
from datetime import datetime


class Block:
    """Represents a single block in the blockchain."""

    def _init_(self, index, transactions, previous_hash, nonce=0):
        self.index = index
        self.timestamp = str(datetime.now())
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        """Generate the SHA-256 hash of the block contents."""
        block_string = json.dumps(self._dict_, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    """A simple Blockchain implementation."""

    difficulty = 3  # Number of leading zeros for Proof of Work

    def _init_(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first (genesis) block in the blockchain."""
        genesis_block = Block(0, [], "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, name, transaction_no, amount):
        """Add a new transaction to pending list."""
        now = datetime.now()
        transaction = {
            "name": name,
            "transaction_no": transaction_no,
            "amount": amount,
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S")
        }
        self.pending_transactions.append(transaction)
        print(f"✅ Transaction added: {transaction}")

    def proof_of_work(self, block):
        """Simple proof-of-work algorithm."""
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def mine_block(self):
        """Mine all pending transactions into a new block."""
        if not self.pending_transactions:
            print("⚠  No transactions to mine.")
            return False

        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.pending_transactions,
            previous_hash=last_block.hash
        )
        new_block.hash = self.proof_of_work(new_block)
        self.chain.append(new_block)
        self.pending_transactions = []
        print(f"⛏  Block #{new_block.index} mined successfully! Hash: {new_block.hash[:20]}...")

    def reset_chain(self):
        """Clear the blockchain and create a new genesis block."""
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()
        print("🗑  Blockchain has been reset.")

    def display_chain(self):
        """Print the blockchain in a readable format."""
        print("\n======= 🧱 BLOCKCHAIN LEDGER =======")
        print(f"Total Blocks: {len(self.chain)}")
        for block in self.chain:
            print(f"\n🔗 Block #{block.index}")
            print(f"Timestamp     : {block.timestamp}")
            print(f"Previous Hash : {block.previous_hash}")
            print(f"Hash          : {block.hash}")
            print(f"Nonce         : {block.nonce}")
            print("Transactions:")
            if not block.transactions:
                print("  - No transactions in this block.")
            else:
                for tx in block.transactions:
                    print(f"  - Name: {tx['name']}, "
                          f"Transaction Number: {tx['transaction_no']}, "
                          f"Amount: ₹{tx['amount']}, "
                          f"Date: {tx['date']}, "
                          f"Time: {tx['time']}")
        print("\n=====================================")


# -------------------------------------------------------------
#  Demo Usage
# -------------------------------------------------------------
if _name_ == "_main_":
    blockchain = Blockchain()

    # Add example transactions
    blockchain.add_transaction("Bhavani", "1234", 120000)
    blockchain.add_transaction("Kiran", "5678", 85000)

    blockchain.mine_block()

    blockchain.add_transaction("Anita", "9012", 45000)
    blockchain.add_transaction("Vijay", "3456", 22000)

    blockchain.mine_block()

    # Display current blockchain
    blockchain.display_chain()

    # Uncomment to reset blockchain
    # blockchain.reset_chain()