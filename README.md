# Layer-2-DAPP-on-top-of-Blockchain
A Dapp, or decentralized application, is a software application that runs on a distributed network.

## How to compile and run the code ?
- Install nodejs, npm, ganache-cli, truffle, web3
- Run the following commands:
    - Open CMD and run: `ganache-cli --gasLimit 1000000000000 --gasPrice 2000`
    - Open another CMD and run: `truffle migrate`
    - A contract will be generated. Copy the `contract address` value and paste it in `deployed_contract_address` value in client.py
        - Eg: 
             
            `> transaction hash:0x344ecd8fbc9c75d4d832294651386b599c9e9365c35c3657131ea888ddcdbc5b`

            `> Blocks: 0             Seconds: 0`

            `> contract address:`     **0x781dA7431D51aA87422d3F46A8fE4EE309e826fD**

            `> block number:         324`

            `> block timestamp:      1681322767`
            `> account:             0x0cD38a03895d35c68A93bdC76c54aFD61509D883`

            `> balance:             99.999999983469576`

            `> gas used:            1273556 (0x136ed4)`

            `> gas price:           0.000002 gwei`

            `> value sent:          0 ETH`

            `> total cost:          0.000000002547112 ETH`
    - Run `python client.py`

## Output
- For every batch of 100 transactions, following is generated:
    - List of failed transactions
    - Successful Transactions
    - Failed Transactions
    - Ratio of successful transactions over total transaction per batch