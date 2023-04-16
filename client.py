import json
from web3 import Web3
import numpy as np
import networkx as nx
import powerlaw
import random
import numpy as np
import time
from utils import generate_power_law_distribution_graph

now = time.time()

#connect to the local ethereum blockchain
provider = Web3.HTTPProvider('http://127.0.0.1:8545')
w3 = Web3(provider)
#check if ethereum is connected
print(w3.is_connected())

#replace the address with your contract address (!very important)
deployed_contract_address = '0x30E0599140818480cb3fb6309E342121b21e9688'

#path of the contract json file. edit it with your contract json file
compiled_contract_path ="build/contracts/Payment.json"
with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']
contract = w3.eth.contract(address = deployed_contract_address, abi = contract_abi)

n = 100
graph = [[0 for i in range(n)] for j in range(n)]

G = generate_power_law_distribution_graph(number_of_nodes=n)
while not nx.is_connected(G):
    G = generate_power_law_distribution_graph(n)

print(G)

for i,j in G.edges():
    graph[i][j], graph[j][i] = 1, 1

for i in graph:
    print(i)

for i in range(n):
    user_registration = contract.functions.registerUser(i+1,'user_{}'.format(i+1)).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
    print(user_registration)

for i in range(n):
    for j in range(i+1, n):
        if(graph[i][j] == 1):
            edge_amount = int(np.round(np.random.exponential(10)+2))
            left_edge = edge_amount//2
            right_edge = edge_amount-left_edge
            # print(left_edge, right_edge, edge_amount)
            joint_acc = contract.functions.createAcc(i+1, j+1, left_edge, right_edge).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})

successful_txn = 0
failed_txn = 0
for i in range(1,1011):
    if(i%101 == 0):
        print('Batch', i/100,':')
        print('Successful Transactions:',successful_txn)
        print('Failed Transactions:', failed_txn)
        print('Ratio:', successful_txn*0.01)
        print()
        successful_txn = 0
        failed_txn = 0
    else:
        acc_1 = random.randint(1,n)
        acc_2 = random.randint(1,n)
        while(acc_1 == acc_2):
            acc_2 = random.randint(1,n)
        # print(acc_1, acc_2)
        isSuccessful, sender_amount_before_transaction = contract.functions.sendAmount(acc_1, acc_2).call()
        # print(isSuccessful)
        if(isSuccessful):
            contract.functions.sendAmount(acc_1, acc_2).transact({'txType':"0x3", 'from':w3.eth.accounts[i%10], 'gas':24096380})
            successful_txn += 1
        else:
            failed_txn += 1
            print("Transaction: " +str(i)+ ": Failed as sender("+str(acc_1)+") account has", sender_amount_before_transaction,"coins before transaction." )

print("\nClosing all the accounts:")
for i in range(1,n+1):
    for j in range(i+1, n+1):
        contract.functions.closeAccount(i,j).transact({'txType':"0x3", 'from':w3.eth.accounts[i%10], 'gas':24096380})

print(time.time()-now)


'''
#Calling a contract function createAcc(uint,uint,uint)
txn_receipt = contract.functions.createAcc(1, 2, 5).transact({'txType':"0x3", 'from':w3.eth.accounts[0], 'gas':2409638})
txn_receipt_json = json.loads(w3.to_json(txn_receipt))
print(txn_receipt_json) # print transaction hash

# print block info that has the transaction)
print(w3.eth.get_transaction(txn_receipt_json)) 

#Call a read only contract function by replacing transact() with call()

'''

#Add your Code here
