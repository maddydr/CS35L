
import React from 'react'
import { useState } from 'react';

function Square({value, onSquareClick}) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}

export default function Board() {
  const [xIsNext, setXIsNext] = useState(true);
  const [squares, setSquares] = useState(Array(9).fill(null));
  const [numMoves, setNumMoves] = useState(0);
  const [oldPos, setOldPos] = useState(-1);
  function handleClick(i) {
    if (calculateWinner(squares) || squares[i] && numMoves < 6) { // if theres a winner already or square has a value and numMoves isnt less than 6 yet aka we should still be placing new moves, don't do anything
      return;
    }

    let nextSquares = squares.slice();
    let validMoves = [[1, 3, 4], [0, 3, 4, 5, 2], [1, 4, 5], 
                      [0, 1, 4, 6, 7], [0, 1, 2, 3, 5, 6, 7, 8], [1, 2, 4, 7, 8], 
                      [3, 4, 7], [6, 3, 4, 5, 8], [7, 4, 5]];
   
    // numMoves > 5, force user to pickup an existing 'X' or 'O' piece and turn it blank
    if (numMoves > 5 && squares[i] !== null){ // at max moves and the square we press has an item in it
      // try to remove an X from the board
      setOldPos(i);
      if (xIsNext && nextSquares[i] === 'X'){ 
       // if we find a valid spot that a user could hypothetically move to, then let the user take move off the board
          nextSquares[i] = null;
          setNumMoves(numMoves => numMoves - 1);
       
      } else if (!xIsNext && nextSquares[i] === 'O'){
          nextSquares[i] = null;
          setNumMoves(numMoves => numMoves - 1);
       
      }
      setSquares(nextSquares);
    }
// need to be able to now add the removed x to any spot, not just the same i index we just used

//  !!!! should be removing an X on X turn, but can click on O and still remove it !!!

    // normal handling of a turn
    if (numMoves <= 5){ 
      // CENTER SQUARE LOGIC for 'X'
      if (oldPos >= 0 && xIsNext && nextSquares[4] === 'X') {
        if (xIsNext) {
          nextSquares[i] = 'X';
        } else {
          nextSquares[i] = 'O';
        }
        let oldSquares = squares.slice();
        let status;
        if (calculateWinner(nextSquares)) {
          setSquares(nextSquares);
          status = 'Winner: ' + winner;
        } else if (oldPos !== 4 && oldPos === i) { // what you picked up was not the center piece and you place it back where you found it
          console.log("HERE 2: ");
          if (xIsNext) {
            nextSquares[i] = 'X';
          } else {
            nextSquares[i] = 'O';
          }
          setSquares(nextSquares);
          setNumMoves(numMoves => numMoves + 1);
          return; // otherwise, means they picked up the center piece, and handle this as a normal move
        }
        // force center square logic for "O"
      } else if (oldPos >= 0 && !xIsNext && nextSquares[4] === 'O') {
        if (xIsNext) {
          nextSquares[i] = 'X';
        } else {
          nextSquares[i] = 'O';
        }
        let oldSquares = squares.slice();
        let status;
        if (calculateWinner(nextSquares)) {
          setSquares(nextSquares);
          status = 'Winner: ' + winner;
        } else if (oldPos !== 4 && oldPos === i) {
          if (xIsNext) {
            nextSquares[i] = 'X';
          } else {
            nextSquares[i] = 'O';
          }
          setSquares(nextSquares);
          setNumMoves(numMoves => numMoves + 1);
          return;
        }
      } else if (oldPos >= 0 && oldPos === i){ // undo feature, should still be same person's turn and put back in same spot
        if (xIsNext) {
          nextSquares[i] = 'X';
        } else {
          nextSquares[i] = 'O';
        }
        setSquares(nextSquares);
        setNumMoves(numMoves => numMoves + 1);
      } else if (oldPos >= 0 && validMoves[oldPos].includes(i)) { // if oldPos is > 0 it means we have more than 6 moves on board
        if (xIsNext) {
          nextSquares[i] = 'X';
        } else {
          nextSquares[i] = 'O';
        }
        setSquares(nextSquares);
        setXIsNext(!xIsNext);
        setNumMoves(numMoves => numMoves + 1);
      } else if (oldPos === -1){
        if (xIsNext) {
          nextSquares[i] = 'X';
        } else {
          nextSquares[i] = 'O';
        }
        setSquares(nextSquares);
        setXIsNext(!xIsNext);
        setNumMoves(numMoves => numMoves + 1);

      }
    }

   
    // separate code for handling if numMoves == 5 because then it can only be placed in certain spots
   
    
  }

  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = 'A winning move was made!      Winner: ' + winner ;
  } else {
    status = 'Next player: ' + (xIsNext ? 'X' : 'O');
  }

  return (
    <>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
        <button onClick={() => handleGoToGameStart(setSquares, setNumMoves, setOldPos, setXIsNext)}>Go to game start</button>
    </>
  );

}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}
function handleGoToGameStart(setSquares, setNumMoves, setOldPos, setXIsNext){
setSquares(Array(9).fill(null)); // Reset the board to the initial state
setNumMoves(0); // Reset the number of moves
setOldPos(-1); // Reset the old position
setXIsNext(true); // Set the first player as 'X' (if that's the initial state)
return;
}