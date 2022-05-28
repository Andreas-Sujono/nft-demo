from brownie import SimpleCollectible, accounts, network, config
from scripts.helpful_scripts import get_publish_source, OPENSEA_FORMAT

sample_token_uri = (
    "https://gateway.pinata.cloud/ipfs/QmVhR8jdtfBuvzAT7GGNrxWF6CuNePVuwfu8RHL5pMBiyk"
)


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    print(network.show_active())
    SimpleCollectible.deploy({"from": dev}, publish_source=get_publish_source())
    simple_collectible = SimpleCollectible[len(SimpleCollectible) - 1]
    token_id = simple_collectible.tokenCounter()
    transaction = simple_collectible.createCollectible(sample_token_uri, {"from": dev})
    transaction.wait(1)
    print(
        "Awesome! You can view your NFT at {}".format(
            OPENSEA_FORMAT.format(simple_collectible.address, token_id)
        )
    )
