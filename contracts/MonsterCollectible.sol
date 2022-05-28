// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

//monster, type + star --> power
contract MonsterCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    enum MonsterType {
        VILLAGER,
        WARRIOR,
        MASTER
    }
    uint256 public maxStar;

    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    mapping(uint256 => MonsterType) public tokenIdToType;
    mapping(uint256 => uint256) public tokenIdToStar;
    mapping(bytes32 => uint256) public requestIdToTokenId;
    event RequestedCollectible(bytes32 indexed requestId);
    // New event from the video!
    event ReturnedCollectible(bytes32 indexed requestId, uint256 randomNumber);

    bytes32 internal keyHash;
    uint256 internal fee;

    constructor(
        address _VRFCoordinator,
        address _LinkToken,
        bytes32 _keyhash
    )
        public
        VRFConsumerBase(_VRFCoordinator, _LinkToken)
        ERC721("ScaryMonster", "SMR")
    {
        tokenCounter = 0;
        maxStar = 5;
        keyHash = _keyhash;
        fee = 0.1 * 10**18;
    }

    function createCollectible(string memory tokenURI)
        public
        returns (bytes32)
    {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        requestIdToTokenURI[requestId] = tokenURI;
        emit RequestedCollectible(requestId);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        address dogOwner = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newItemId = tokenCounter;
        _safeMint(dogOwner, newItemId);
        _setTokenURI(newItemId, tokenURI);

        uint256 newRandomNumber = randomNumber * now;

        MonsterType monsterType = MonsterType(randomNumber % 3);
        uint256 monsterStar = newRandomNumber % maxStar;
        tokenIdToType[newItemId] = monsterType;
        tokenIdToStar[newItemId] = monsterStar + 1;
        requestIdToTokenId[requestId] = newItemId;
        tokenCounter = tokenCounter + 1;

        emit ReturnedCollectible(requestId, randomNumber);
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
