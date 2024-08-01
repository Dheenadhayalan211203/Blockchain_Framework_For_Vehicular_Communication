import hashlib
import json
import datetime

from simulation import currentGreen, currentYellow, signals, vehicles, directionNumbers, timeElapsed, noOfSignals

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256((str(self.index) + str(self.timestamp) + json.dumps(self.data) + str(self.previous_hash) + str(self.nonce)).encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print("Block mined:", self.hash)

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)



    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

# Simulated data for a block
simulation_data = {
    "current_green": currentGreen,
    "current_yellow": currentYellow,
    "signal_timers": [signals[i].signalText for i in range(noOfSignals)],
    "vehicle_counts": [vehicles[directionNumbers[i]]['crossed'] for i in range(noOfSignals)],
    "time_elapsed": timeElapsed
}

# Create blockchain and add simulated data as blocks
blockchain = Blockchain()
for i in range(5):  # Example: Add 5 blocks
    new_block = Block(i + 1, datetime.datetime.now(), simulation_data, blockchain.get_latest_block().hash)
    blockchain.add_block(new_block)

# Print blockchain details
print("Blockchain validity:", blockchain.is_chain_valid())
for block in blockchain.chain:
    print("", block.index)
