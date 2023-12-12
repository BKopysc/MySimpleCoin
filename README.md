# MySimpleCoin
Simple Coin blockchain implementation for IT course

# Installation 
pip install -r requirements.txt

# Usage
1. Activate env: env/Scripts/activate

# Protocol

Nodes can communicate with each other by methods:

1. Send new block

`{'_type': 'new_block', 'block': {block_obj} }`

2. Send transaction

`{'_type': 'new_transaction', 'transaction': {trans_obj}}:`

3. Pop transaction

`{'_type': 'pop_transaction', 'transaction': transaction_id}`

4. New Blockchain

`{'_type': 'new_blockchain', 'blockchain': {blockchain_obj}}:`
