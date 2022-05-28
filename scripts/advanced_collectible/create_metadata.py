#!/usr/bin/python3
import os
import requests
import json
from brownie import MonsterCollectible, network
from metadata import sample_metadata
from scripts.helpful_scripts import get_monster_type
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

to_image_uri = {
    "VILLAGER": "https://gateway.pinata.cloud/ipfs/QmfUY8XnM9sZec3huJvwRsvPNpzrTGxMMF3L6aee4XnCGY",
    "WARRIOR": "https://gateway.pinata.cloud/ipfs/QmYdpVYY1oZMAxnXE21Vw8D98KVVsnDoHedV9S7j9AVHzn",
    "MASTER": "https://gateway.pinata.cloud/ipfs/QmSJq64aaxPWLC7NnHPq5ymNXDbDZousZg6iFVRPmC6JUP",
}


def main():
    print("Working on " + network.show_active())
    monster_nft = MonsterCollectible[-1]
    number_of_monster_nfts = monster_nft.tokenCounter()
    print("The number of tokens you've deployed is: " + str(number_of_monster_nfts))
    write_metadata(number_of_monster_nfts, monster_nft)


def write_metadata(token_ids, nft_contract):
    for token_id in range(token_ids):
        collectible_metadata = sample_metadata.metadata_template
        monsterType = get_monster_type(nft_contract.tokenIdToType(token_id))
        metadata_file_name = (
            "./metadata/{}/".format(network.show_active())
            + str(token_id)
            + "-"
            + monsterType
            + ".json"
        )
        if os.path.exists(metadata_file_name):
            print(
                "{} already found, delete it to overwrite!".format(metadata_file_name)
            )
        else:
            print("Creating Metadata file: " + metadata_file_name)
            collectible_metadata["name"] = get_monster_type(
                nft_contract.tokenIdToType(token_id)
            )
            collectible_metadata["description"] = "A scary {} monster!".format(
                collectible_metadata["name"]
            )
            image_to_upload = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_path = "./img/{}.png".format(
                    monsterType.lower().replace("_", "-")
                )
                image_to_upload = upload_to_ipfs(image_path)
            image_to_upload = (
                to_image_uri[monsterType] if not image_to_upload else image_to_upload
            )
            collectible_metadata["image"] = image_to_upload
            print("final data: ", collectible_metadata)
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


# curl -X POST -F file=@metadata/rinkeby/0-SHIBA_INU.json http://localhost:5001/api/v0/add


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = (
            os.getenv("IPFS_URL") if os.getenv("IPFS_URL") else "http://localhost:5001"
        )
        response = requests.post(ipfs_url + "/api/v0/add", files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = "ipfs://{}?filename={}".format(ipfs_hash, filename)
        print(image_uri)
    return image_uri
