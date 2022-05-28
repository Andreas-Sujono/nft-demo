#!/usr/bin/python3
from brownie import MonsterCollectible, network, config
from scripts.helpful_scripts import (
    fund_with_link,
    get_publish_source,
    get_account,
    get_contract,
)


def deploy_contract():
    dev = get_account()
    print(network.show_active())
    monster_nft = MonsterCollectible.deploy(
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["keyhash"],
        # config["networks"][network.show_active()]["fee"],
        {"from": dev},
        publish_source=get_publish_source(),
    )
    return monster_nft


def main():
    monster_nft = deploy_contract()
    fund_with_link(monster_nft.address)
    return monster_nft
