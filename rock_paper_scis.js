function gamePlay(){
    play = confirm("Would you like to play Rock, Paper, Scissors?");
    return play;
}


function choice(){
    var turn = prompt("Rock, Paper, or Scissors?");
    return turn;
}


function opChoice(){
    var rand = Math.floor((Math.random() * 3) + 1);
    if (rand == 1 ){
        return "Rock";
    }
    else if (rand == 2){
        return "Paper";
    }
    else{
        return "Scissors";
    }
}


play = gamePlay();
while (play == true){
    var user = choice();
    var op = opChoice();
    
    console.log("You chose: " + user);
    console.log("Computer chose: " + op)
    
    if (user == op){
        console.log("The game was a tie! Play again!");
    }
    else if (user == "Rock" && op == "Scissors" || user == "Scissors" && op == "Paper" || user = "Paper" && op == "Rock"){
        console.log("You win the game!");
    }
    else{
        console.log("You lost the game. :(");
    }
    var play = window.setTimeout(gamePlay, 2000);
}
