# review system
# config file for the review contract.

from web3 import Web3, HTTPProvider, IPCProvider

# Network location
w3 = Web3(HTTPProvider('http://10.1.1.32:8545'))

# Address
contract_address = '0x172794aff82ABF54F626e7D6C25aE0B6772E39F0'

# Logic Code 
contract_source_code = '''
pragma solidity ^0.4.0;
contract reviewSystem {
    //confirmed review sub structure
    struct review {
        uint8 rating;
        string content;
        uint96 epc;
    }
    struct product {
        review[] pReviews;
    }
    
    //confirmed review structure
    mapping (uint96 => product) products;
    mapping (uint96 => bool) reviewed_items; //product reviewed
    
    //notaries structure
    uint32 notaries_count = 0;
    mapping (address => bool) registered_notaries; //epc => if registered
    
    //unconfirmed queue structure
    struct Unconf_review { //unconfirmed review
        bool received;
        uint96 epc;
        bytes ownersig;
        uint8 rating;
        string content;
        
        uint32 accept_count;
        uint32 reject_count;
        mapping (address => bool) notaries;
    }
    mapping (uint96 => Unconf_review) uReviews;
    
    //constructor, admin
    address admin;
    function reviewSystem() public{
        admin = msg.sender;
    }
    function contractAdmin() public constant returns (address) {
        return admin;
    }
    
    //notary management
    function notaryRegister(address newNotary) external {
        require(msg.sender == admin);
        require(registered_notaries[newNotary] != true);

        registered_notaries[newNotary] = true;
        notaries_count++;
    }
    function notaryRemove(address notary) external {
        require(msg.sender == admin);
        require(registered_notaries[notary] == true);
    
        delete registered_notaries[notary];
        notaries_count--;
    }
    //notary get functions
    function notaryCount() constant public returns (uint32) {
        return notaries_count;
    }
    
    //unconfirmed reviews get functions
    function uReviewStatus(uint96 epc) external constant returns(bool, uint32, uint32) {
        return (uReviews[epc].received, uReviews[epc].accept_count, uReviews[epc].reject_count);
    }
    
    //unconfirmed reviews external functions
    event NewReviewSubmitted(uint96 epc, bytes ownersig, uint time);
    function adduReview(uint96 epc, bytes ownersig, uint8 rating, string content) external {
        //check
        require(reviewed_items[epc] != true); //not reviewed before
        require(uReviews[epc].epc == 0);
        require(ownersig.length == 64);
        
        //add to queue
        uReviews[epc].epc = epc;
        uReviews[epc].ownersig = ownersig;
        uReviews[epc].rating = rating;
        uReviews[epc].content = content;
        uReviews[epc].received = true;
        
        //emit
        NewReviewSubmitted(epc, ownersig, now);
    }
    
    //notaries vote
    event NotaryVoted(uint96 epc, uint time);
    function notarySendResult(uint96 epc, bool result) external {
        //check
        require(registered_notaries[msg.sender] == true); //a real notary
        require(uReviews[epc].epc == epc); // in queue
        require(uReviews[epc].notaries[msg.sender] == false); //not double vote
        
        //add result
        if (result == true) {
            uReviews[epc].accept_count++;
        } else {
            uReviews[epc].reject_count++;
        }
        uReviews[epc].notaries[msg.sender] = true;
        
        //update queue
        uint32 threshold = notaries_count/2;
        if (uReviews[epc].accept_count > threshold) {
            addrReview(epc>>38, epc, uReviews[epc].rating, uReviews[epc].content);
            delete uReviews[epc];
        } else if (uReviews[epc].reject_count >= threshold) {
            delete uReviews[epc];
        }
        NotaryVoted(epc, now);
    }
    
    //confirmed functions
    event ReviewConfirmed(uint96 epc, uint time);
    function addrReview(uint96 id, uint96 epc, uint8 rating, string content) internal {
            products[id].pReviews.length++;
            products[id].pReviews[products[id].pReviews.length - 1].rating = rating;
            products[id].pReviews[products[id].pReviews.length - 1].content = content;
            products[id].pReviews[products[id].pReviews.length - 1].epc = epc;

            reviewed_items[epc] = true;
            ReviewConfirmed(epc, now);
    }
    
    //review get functions
    function getReviewCount(uint96 id) public constant returns(uint256) {
        return products[id].pReviews.length;
    }
    function getReview(uint96 id, uint32 index) public constant returns(uint8, string, uint96) {
        return (products[id].pReviews[index].rating, products[id].pReviews[index].content, products[id].pReviews[index].epc);
    }
}
'''
