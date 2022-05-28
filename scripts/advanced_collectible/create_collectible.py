#!/usr/bin/python3
from brownie import MonsterCollectible, accounts, config
from scripts.advanced_collectible.deploy_advanced import deploy_contract
from scripts.helpful_scripts import (
    get_monster_type,
    fund_with_link,
    listen_for_event,
    get_account,
)
import time


def main():
    dev = get_account()
    monster_nft = (
        MonsterCollectible[-1]
        if MonsterCollectible and MonsterCollectible[-1]
        else deploy_contract()
    )
    # fund_with_link(monster_nft.address)
    transaction = monster_nft.createCollectible("None", {"from": dev})
    print("Waiting on second transaction...")

    # wait for the 2nd transaction
    transaction.wait(1)
    # time.sleep(35)
    listen_for_event(monster_nft, "ReturnedCollectible", timeout=200, poll_interval=10)

    requestId = transaction.events["RequestedCollectible"]["requestId"]
    token_id = monster_nft.requestIdToTokenId(requestId)
    monster_type = get_monster_type(monster_nft.tokenIdToType(token_id))
    monster_star = monster_nft.tokenIdToStar(token_id)
    print(
        "monster type of tokenId {} is {} with star {}, contract address: {}".format(
            token_id, monster_type, monster_star, monster_nft
        )
    )
