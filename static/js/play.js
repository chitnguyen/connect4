/**
 * Created by Chinguyen on 28/10/2016.
 */
var gameField = new Array();

function checkForVictory(player, row, col){
      gameField[row][col] = player;
      if(getAdj(row,col,0,1)+getAdj(row,col,0,-1) > 2){
          return true;
      } else {
          if(getAdj(row,col,1,0) > 2){
              return true;
          } else {
              if(getAdj(row,col,-1,1)+getAdj(row,col,1,-1) > 2){
                  return true;
              } else {
                  if(getAdj(row,col,1,1)+getAdj(row,col,-1,-1) > 2){
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
        return 1+getAdj(row+row_inc, col+col_inc, row_inc, col_inc);
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

function firstFreeRow(col){
  for(var i = 0; i<6; i++){
      if(gameField[i][col]!=0){
          break;
      }
  }
  return i-1;
}

//create a 6x7 board with 0 entries
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
        gameField[rows[i]][cols[i]] = players[i];
        var color = (players[i] == player1) ? 'red' : 'yellow';
        var id = "btn"+rows[i].toString()+cols[i].toString();
        var button = document.getElementById(id);
        button.style.cssText += 'background-color: ' + color
    }
}
