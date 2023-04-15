// SPDX-License-Identifier: MIT
pragma solidity >=0.8.2 <0.9.0;
//pragma solidity ^0.8.0;

/*@custom:dev-run-script NatSpec
*/
contract Payment {

   mapping(uint => string) public users;
uint[] ids;
uint[] public path;
   mapping (uint => mapping (uint=>uint)) public joint_account;
    mapping(uint => uint[]) public adj_mat; 
    uint public total_nodes;
    struct Node {
        uint parent; // Parent node
        bool visited; // Flag to track visited user_nodes
    }
    mapping(uint => Node) public user_nodes;



   //function to register user
   function registerUser(uint use_id, string memory user_name) public returns (uint)
   {
       total_nodes=total_nodes+1;
       users[use_id]=user_name;
       ids.push(use_id);
       return use_id;
   }

   //create account between user1 and user
   function createAcc(uint user_id_1,uint user_id_2,uint balance1,uint balance2) public returns(uint)
   {
       //stores balance between user1 and user2
       joint_account[user_id_1][user_id_2]=balance1;
       joint_account[user_id_2][user_id_1]=balance2;
       uint[] storage existingValues1 = adj_mat[user_id_1];
       existingValues1.push(user_id_2);
       adj_mat[user_id_1]=existingValues1;
       uint[] storage existingValues2 = adj_mat[user_id_2];
       existingValues2.push(user_id_1);
       adj_mat[user_id_2]=existingValues2;
       return joint_account[user_id_1][user_id_2];
   }

    //function to send amount from user1 and user2
    function sendAmount(uint user_id_1,uint user_id_2) public returns(bool, uint)
    {
        //stores if there is path between the users or not
        uint amount = 1;
        bool ispath;
        delete path;
        ispath=check_path(user_id_1,user_id_2);
        if(!ispath) return (false,1000000);

        //populate the path with users which are between user1 and user2 in shortest path 
        uint curr=user_id_2;
        while(curr!=user_id_1)
        {
            path.push(curr);
            curr=getParent(curr);
        }
        path.push(user_id_1);

        //check if the trasaction can be possible
        bool decision = true;
        for(uint j=path.length - 1; j>=1; j--){
            if(joint_account[path[j]][path[j-1]] < amount){
                decision = false;
                return (decision,joint_account[path[j]][path[j-1]]);
            }
        }

        //transfer the amount between the users 
        for(uint j=path.length - 1; j>=1; j--){
            joint_account[path[j]][path[j-1]] -= amount;
            joint_account[path[j-1]][path[j]] += amount;
        }
        return (true, joint_account[path[path.length-1]][path[path.length-2]] + amount);
        // return path;
        
    }

    //check if there path exist from user1 and user2
    function check_path(uint start,uint end) public returns (bool)
    {


        for(uint i=0;i<total_nodes;i++)
        {
            user_nodes[ids[i]].parent=0;
            user_nodes[ids[i]].visited=false;

        }

        uint[] memory queue = new uint[](total_nodes);
        uint f = 0;
        uint r = 0;

        //BFS algorithm
        if(start==end)
        {
            return true;
        }

        queue[r++] = start;
        user_nodes[start].parent = 0;
        user_nodes[start].visited = true; 

        while (f < r) {
            uint current = queue[f++];

             if (current == end) {
                return true;
            }
            //get all the neighbouring nodes
             for (uint i = 0; i < adj_mat[current].length; i++) {
                 uint neighbor = adj_mat[current][i];

                //check if the nodes are already visited
                if (! user_nodes[neighbor].visited) {
                    queue[r++] = neighbor;
                    user_nodes[neighbor].visited = true;
                    user_nodes[neighbor].parent = current; 

                }
            }

        }
        return false;

    }

    //get parent of the node in the bfs path
    function getParent(uint node) public view returns (uint) {
        return user_nodes[node].parent;
    }

    //close account between user1 and user2
    function closeAccount(uint user_id_1, uint user_id_2) public
    {
        delete joint_account[user_id_1][user_id_2];
        delete joint_account[user_id_2][user_id_1];

    }

}