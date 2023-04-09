import json
from web3 import Web3
import numpy as np
import networkx as nx
import powerlaw


#connect to the local ethereum blockchain
provider = Web3.HTTPProvider('http://127.0.0.1:8545')
w3 = Web3(provider)
#check if ethereum is connected
print(w3.is_connected())

#replace the address with your contract address (!very important)
deployed_contract_address = '0xe61266cd38b0bF096d509190A8ef034525b6CeCf'

#path of the contract json file. edit it with your contract json file
compiled_contract_path ="build/contracts/Payment.json"
with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']
contract = w3.eth.contract(address = deployed_contract_address, abi = contract_abi)


def generate_power_law_distribution_graph(number_of_nodes:int):
    """ generate and return a graph following power law degree distribution 

    Args:
        number_of_nodes (int): number of nodes

    Returns:
        G: a graph following power law degree distribution
    """
    
    # Generate a power law distribution with alpha=2.5 and xmin=1
    pl_dist = powerlaw.Power_Law(xmin=1, parameters=[2.5])

    # Generate samples from the distribution
    samples = pl_dist.generate_random(number_of_nodes)

    degree_sequence = [int(i) for i in samples]
    degree_sequence.sort(reverse=True)

    G = nx.Graph()
    for i in range(number_of_nodes):
        for j in range(i + 1, number_of_nodes):
            if (degree_sequence[i] > 0 and degree_sequence[j] > 0):
                degree_sequence[i] -= 1
                degree_sequence[j] -= 1
                G.add_edge(i, j)
                G.add_edge(j, i)
    return G

n = 100
G = generate_power_law_distribution_graph(number_of_nodes=n)
while not nx.is_connected(G):
    G = generate_power_law_distribution_graph(n)

for i in range(1,101):
    user_registration = contract.functions.registerUser(i,'user_{}'.format(i))
print(user_registration)

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
