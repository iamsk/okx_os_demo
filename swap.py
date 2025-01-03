import json
import time
from util import send_request
from wallet import broadcast_transaction

"""
兑换API
"""


def query_supported_chain():
    """
    https://www.okx.com/api/v5/dex/aggregator/supported/chain
    :return:
    """
    url = "/api/v5/dex/aggregator/supported/chain"
    resp = send_request(url, method="GET")
    return resp.json()


def save_supported_chain():
    chains = query_supported_chain()['data']
    data = [{x['chainName']: x for x in chains}]
    with open('chains.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def query_supported_tokens(chainId):
    """
    获取币种列表。此接口的返回结果是欧易 DEX 认为的主流代币和平台代币。你可以指定该列表之外的代币在欧易 DEX 询价和兑换。
    :return:
    """
    url = "/api/v5/dex/aggregator/all-tokens"
    data = {
        "chainId": chainId
    }
    resp = send_request(url, method="GET", params=data)
    return resp.json()


def get_liquidity(chainId):
    """
    获取欧易 DEX 聚合器协议支持兑换的流动性列表。

    :param chainId:
    :return:
    """
    url = "/api/v5/dex/aggregator/get-liquidity"
    data = {
        "chainId": chainId
    }
    resp = send_request(url, method="GET", params=data)
    return resp.json()


def approve_transaction(chainId, tokenContractAddress, approveAmount):
    """
    根据 ERC-20 Token 标准，在执行兑换交易前用户需要授权欧易 DEX router 对其钱包进行资产操作，此接口提供发起授权交易前所需要的交易信息。
    """
    url = "/api/v5/dex/aggregator/approve-transaction"
    data = {
        "chainId": chainId,
        "tokenContractAddress": tokenContractAddress,
        "approveAmount": approveAmount
    }
    resp = send_request(url, method="GET", params=data)
    return resp.json()


def quote(chainId, amount, fromTokenAddress, toTokenAddress, dexIds=None,
          priceImpactProtectionPercentage=None, feePercent=None):
    """
    通过 DEX 聚合器获取最优报价。

    :param chainId: 链 ID
    :param amount: 币种询价数量 (数量需包含精度，如兑换 1.00 USDT 需输入 1000000，兑换 1.00 DAI 需输入 1000000000000000000)
    :param fromTokenAddress: 询价币种合约地址 (如0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee)
    :param toTokenAddress: 目标币种合约地址 (如0xa892e1fef8b31acc44ce78e7db0a2dc610f92d00)
    :param dexIds: dexIds 限定询价的流动性池 dexId , 多个组合按 , 分隔 (如 1,50,180 ，更多可查看流动性列表)
    :return:
    """
    url = "/api/v5/dex/aggregator/quote"
    data = {
        "chainId": chainId,
        "amount": amount,
        "fromTokenAddress": fromTokenAddress,
        "toTokenAddress": toTokenAddress,
        "dexIds": dexIds,
        "priceImpactProtectionPercentage": priceImpactProtectionPercentage,
        "feePercent": feePercent
    }
    resp = send_request(url, method="GET", params=data)
    return resp.json()


def swap(chainId, amount, fromTokenAddress, toTokenAddress, slippage, userWalletAddress):
    """
    通过 DEX 聚合器 router 获取兑换所需的交易数据。
    :param chainId:
    :param amount:
    :param fromTokenAddress:
    :param toTokenAddress:
    :param slippage:
    :param userWalletAddress:
    :return:
    """
    url = "/api/v5/dex/aggregator/swap"
    data = {
        "chainId": chainId,
        "amount": amount,
        "fromTokenAddress": fromTokenAddress,
        "toTokenAddress": toTokenAddress,
        "slippage": slippage,
        "userWalletAddress": userWalletAddress
    }
    resp = send_request(url, method="GET", params=data)
    return resp.json()


if __name__ == '__main__':
    # save_supported_chain()
    # exit()

    # 8453 stands for Base Chain
    # data = query_supported_tokens("8453")
    data = approve_transaction("8453", "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913", 1000000)
    print(json.dumps(data, indent=2, ensure_ascii=False))
    time.sleep(1)
    # exit()
    # buy virtual with usdc
    # data = quote("8453", 1000000, '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913', '0x0b3e328455c4059eeb9e3f84b5543f74e24e7e1b')
    # print(json.dumps(data, indent=2, ensure_ascii=False))
    # exit()
    # data = get_liquidity("8453")
    data = swap("8453", 1000000, '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913', '0x0b3e328455c4059eeb9e3f84b5543f74e24e7e1b', 0.01, '0x42c891fe3799fac46c3b82e95cc5a22a288e3178')
    tx = data['data'][0]['tx']['data']
    print(json.dumps(data, indent=2, ensure_ascii=False))
    time.sleep(1)
    data = broadcast_transaction(tx, "8453", '0x42c891fe3799fac46c3b82e95cc5a22a288e3178')
    print(json.dumps(data, indent=2, ensure_ascii=False))
    # print(json.dumps(data, indent=2, ensure_ascii=False))
