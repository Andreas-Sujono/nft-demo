// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

//monster, type + star --> power
contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;

    constructor() public ERC721("TestNFT", "TST") {
        tokenCounter = 0;
    }

    function createCollectible(string memory tokenURI)
        public
        returns (uint256)
    {
        _safeMint(msg.sender, tokenCounter);
        _setTokenURI(tokenCounter, tokenURI);
        tokenCounter += 1;
        return tokenCounter - 1;
    }
}
