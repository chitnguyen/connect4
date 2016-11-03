/**
 * Created by Chinguyen on 28/10/2016.
 */

function removeBorder() {
    for (var i = 0; i < 6; i++) {
        for (var j = 0; j < 7; j++) {
            var id = 'btn' + String(i) + String(j);
            var last_button = document.getElementById(id);
            last_button.style.cssText += 'border: none';
        }
    }
}

// With each move, we will check whether there is a winner
function checkForVictory(player, row, col) {
    //  Update gameField with player id and check for 4 coins
    gameField[row][col] = player;
    if(getAdj(row, col, 0, 1) + getAdj(row, col, 0, -1) > 2) {
        return true;
    } else {
        if(getAdj(row, col, 1, 0) > 2){
            return true;
        } else {
            if(getAdj(row, col, -1, 1)+getAdj(row, col, 1,-1) > 2){
                return true;
            } else {
                if(getAdj(row, col, 1, 1)+getAdj(row, col, -1, -1) > 2){
                    return true;
                } else {
                  return false;
              }
            }
        }
    }
}

function getAdj(row, col, row_inc, col_inc){
    if(cellVal(row, col) == cellVal(row + row_inc, col + col_inc)){
        return 1 + getAdj(row+row_inc, col+col_inc, row_inc, col_inc);
    } else {
        return 0;
    }
}

function cellVal(row, col){
    if(gameField[row] == undefined || gameField[row][col] == undefined){
        return -1;
    } else {
        return gameField[row][col];
  }
}
// This allows us to automatically find the first free/available row for each column.
function firstFreeRow(col) {
  for(var i = 0; i<6; i++){
      if(gameField[i][col]!=0){
          break;
      }
  }
  return i-1;
}

//Initialise 6x7 board with 0 entries. Later on, after each move, we will update to player id
function prepareField() {
    gameField = new Array();
    for(var i=0; i<6; i++) {
        gameField[i] = new Array();
        for(var j=0; j<7; j++){
            gameField[i].push(0);
        }
    }
}

// Filling the board with all the moves
function updateCurrentField(players, rows, cols, player1){
    var n = players.length;
    for(var i=0; i<n; i++) {
        placeCoin(players[i], rows[i], cols[i], player1)
    }
}

function placeCoin(player, row, col, player1) {
    gameField[row][col] = player;
    // Auto-assign player who created game (player1) with red and yellow for player2
    var color = (player == player1) ? 'red' : 'yellow';
    var id = "btn" + row.toString() + col.toString();
    var button = document.getElementById(id);
    button.style.cssText += 'background-color: ' + color
}

// Create a 6 rows x 7 columns board
var table = document.createElement("table");
table.setAttribute('id', 'board');
// create 6 rows and for each row create 7 columns
for (var i= 0; i<6; i++) {
    var tr = document.createElement('tr');
    for (var j = 0; j < 7; j++){
        var td = document.createElement('td');
        //each coordinate is a button
        var button = document.createElement('button');
        button.setAttribute('class', 'btn');
        button.setAttribute('id', 'btn'+String(i)+String(j));
        button.setAttribute('data-row', String(i));
        button.setAttribute('data-col', String(j));
        td.appendChild(button);
        tr.appendChild(td)
    }
    table.appendChild(tr)
}
document.body.appendChild(table);

