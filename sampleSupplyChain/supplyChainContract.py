# supply chain system(simplified version)
# config file for the supplychain contract.

from web3 import Web3, HTTPProvider, IPCProvider

sw3 = Web3(HTTPProvider('http://10.1.1.32:8546'))
scontract_address = '0xf2a94a9cb3A1802b029E9caFC400e94f747cDE4E'
supply_source_code = '''
pragma solidity ^0.4.0;
contract supplyChain {
    enum ProductStatus {Shipped, Owned, Disposed}
    struct ProductInfo {
        bytes owner;
        address recipient;
        ProductStatus status;
        uint creationTime;
        uint8 nTransferred;
    }

    mapping (uint96 => ProductInfo) products;

    function enrollProduct(uint96 EPC, bytes owner) public{
        products[EPC].owner = owner;
        products[EPC].status = ProductStatus.Owned;
        products[EPC].creationTime = now;
        products[EPC].nTransferred = 1;
    }

    function getCurrentOwner(uint96 EPC) public constant returns (bytes) {
        return products[EPC].owner;
    }

    function getnTransferred(uint96 EPC) public constant returns (uint8) {
        return products[EPC].nTransferred;
    }

    function getcreationTime(uint96 EPC) public constant returns (uint) {
        return products[EPC].creationTime;
    }
}
'''
