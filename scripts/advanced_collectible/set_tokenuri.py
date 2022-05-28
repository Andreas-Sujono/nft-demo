#!/usr/bin/python3
from brownie import MonsterCollectible, accounts, network, config
from metadata import sample_metadata
from scripts.helpful_scripts import get_monster_type, OPENSEA_FORMAT, get_account


metadata_dic = {
    "VILLAGER": "https://gateway.pinata.cloud/ipfs/QmPfP684ibj7mNzsjFaHLuwCBaXeqam9jsbTBDGWuNLxmc",
    "WARRIOR": "https://gateway.pinata.cloud/ipfs/QmVhR8jdtfBuvzAT7GGNrxWF6CuNePVuwfu8RHL5pMBiyk",
    "MASTER": "https://gateway.pinata.cloud/ipfs/QmVhR8jdtfBuvzAT7GGNrxWF6CuNePVuwfu8RHL5pMBiyk",
}


def main():
    print("Working on " + network.show_active())
    monster_nft = MonsterCollectible[len(MonsterCollectible) - 1]
    number_of_monster_nfts = monster_nft.tokenCounter()
    print("The number of tokens you've deployed is: " + str(number_of_monster_nfts))
    for token_id in range(0, number_of_monster_nfts):
        type = get_monster_type(monster_nft.tokenIdToType(token_id))
        if not monster_nft.tokenURI(token_id).startswith("https://"):
            print("Setting tokenURI of {}".format(token_id))
            set_tokenURI(token_id, monster_nft, metadata_dic[type])
        else:
            print("Skipping {}, we already set that tokenURI!".format(token_id))


def set_tokenURI(token_id, nft_contract, tokenURI):
    dev = get_account()
    nft_contract.setTokenURI(token_id, tokenURI, {"from": dev})
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(nft_contract.address, token_id)
        )
    )
    print('Please give up to 20 minutes, and hit the "refresh metadata" button')
