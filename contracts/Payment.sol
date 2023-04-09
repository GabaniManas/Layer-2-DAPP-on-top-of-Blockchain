// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Payment {
  constructor() public {
  }

  struct User {
      uint userId;
      string userName;
  }

  mapping(address => User) users;

  function registerUser(uint user_id, string memory user_name) public {
    users[msg.sender] = User(user_id, user_name);
  }

  function createAcc(uint user_id_1, uint user_id_2, uint balance) public {
    
  }

  function sendAmount(uint user_id_1, uint user_id_2) public payable {
    
  }

  function closeAccount(uint user_id_1, uint user_id_2) public payable {
    
  }
}
