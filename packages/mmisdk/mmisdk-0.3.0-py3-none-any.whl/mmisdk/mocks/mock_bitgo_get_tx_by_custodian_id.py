MOCK_BITGO_GET_TX_BY_CUSTODIAN_ID = {
    "data": [
        {
            "transactionStatus": "created",
            "custodianTransactionId": "95851701-e573-497a-9df8-fbca8bbf80e9",
            "from": "0xb22505ee2aac7d52d4a218f5877cdbae3bbeec75",
            "to": "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
            "coin": "gteth",
            "value": "1000000000000000000",
            "gasLimit": "260849",
            "userId": "5e822adc91a83a3f00975fa72b5a536d",
            "createdTime": "2022-03-29T01:12:10.016Z",
            "data": "0x7ff36ab500000000000000000000000000000000000000000000000006d5dbf25e950f2f0000000000000000000000000000000000000000000000000000000000000080000000000000000000000000b22505ee2aac7d52d4a218f5877cdbae3bbeec7500000000000000000000000000000000000000000000000000000000624263dd0000000000000000000000000000000000000000000000000000000000000002000000000000000000000000b4fbf271143f4fbf7b91a5ded31805e42b2208d60000000000000000000000001f9840a85d5af5bf1d1762f925bdaddc4201f984",
            "transactionHash": "0x2b81204f61c7736cb4b9cf89b842d44081b476f35e521fb745d8e212c02b77b4",
            "decodedData": {
                    "protocolName": "SushiswapV2Router",
                    "decoderType": "supportedProtocol",
                    "methodSignature": "swapExactETHForTokens(uint256,address[],address,uint256)",
                    "methodParameters": [
                        {
                                    "name": "amountOutMin",
                                    "type": "uint256",
                                    "value": {
                                            "_hex": "0x06d5dbf25e950f2f",
                                            "_isBigNumber": True
                                    },
                            "_id": "62425ceae5fd64ada50ad476"
                        },
                        {
                            "name": "path",
                            "type": "address[]",
                                    "value": [
                                        "0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6",
                                        "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"
                                    ],
                            "_id": "62425ceae5fd64ada50ad477"
                        },
                        {
                            "name": "to",
                            "type": "address",
                                    "value": "0xB22505ee2aac7d52d4A218F5877CdBaE3BbeEC75",
                                    "_id": "62425ceae5fd64ada50ad478"
                        },
                        {
                            "name": "deadline",
                            "type": "uint256",
                                    "value": {
                                        "_hex": "0x624263dd",
                                        "_isBigNumber": True
                                    },
                            "_id": "62425ceae5fd64ada50ad479"
                        }
                    ],
                "_id": "62425ceae5fd64ada50ad475"
            }
        }
    ],
    "_meta": {
        "reqId": "unk-iv73f8cadhyhsv3f8chr"
    }
}
