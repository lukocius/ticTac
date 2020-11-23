import React, { Component } from "react";
import Board, {generateGridNxN} from "./Board";


// game state: 
//     board state size*size X size*size grid of values X, O or null
//     move state: Player to move (X or O),
//          valid moves based on the last move
//          local wins state, outer board size*size grid of values X, O or null
//     win state: If winner is known, no move is valid.
//     if no move is valid, game over.



export default class Game extends Component
{
    constructor(props)
    {
        super(props);
        // Game state (board state + move state (+ win state)).
        this.state = {
          squares: Array(this.props.size*this.props.size).fill(
            Array( this.props.size*this.props.size).fill(null)),
          localWinners: Array(
            this.props.size * this.props.size).fill(null),
          lastMoveLocation: {row: null, col: null, outerRow: null, outerCol:null},
          xIsNext: true,
          winner: null
        }
        this.renderBoard=this.renderBoard.bind(this);
    }

    // return true if move on the board idx is valid.
    isBoardValid(idx)
    {
        // board is complete, no move is valid.
        if (this.state.winner)
            return false;

        const lastRow = this.state.lastMoveLocation.row;
        const lastCol = this.state.lastMoveLocation.col;

        // Not initialised. Valid.
        if (lastRow === null || lastCol === null)
        {
            return true;
        }
        else
        {
            const currentBoard = lastRow * this.props.size + lastCol;
            if (this.state.localWinners[currentBoard])
            {
                // If local board is complete, next move
                // is available in any non-complete board.
                return this.state.localWinners[idx] === null;
            }
            else
            {
                return idx === currentBoard;
            }
        }
    }

    handleClick(inner_index, outer_index)  //size*size x size*size grid position.
    {
        const size = this.props.size;
        // Copy outer and inner boards.
        var outerSquares = this.state.squares.slice();
        var squares = this.state.squares[outer_index].slice();
        var localWinners = this.state.localWinners.slice();
        
        // If not clickable - do nothing.
        if (this.state.winner || !this.isBoardValid(outer_index) || squares[inner_index])
        {
            return;
        }
        // else place a mark and update board state.
        squares[inner_index] = this.state.xIsNext ? 'X' : 'O';
        outerSquares[outer_index] = squares;

        // update last move location
        const lastMoveLocation = {
            row: ~~(inner_index/size),
            col: inner_index % size,
            outerRow: ~~(outer_index/size),
            outerCol: outer_index % size
        } 

        // check for local winner in current board (or draw).
        localWinners[outer_index] = this.calculateWinner(squares, lastMoveLocation);
        
        // check for global winner (or draw).
        const winner = null;


        this.setState((prevState, props) => ({
            squares: outerSquares,
            localWinners: localWinners,
            lastMoveLocation: lastMoveLocation,
            xIsNext: !this.state.xIsNext,
            winner: winner
        }))
    }
    
    calculateWinner(squares, lastMoveLocation){
        // First move - no winner.
        if (!lastMoveLocation)
            return null;

        // This can be static function. Size already given.
        const size = Math.sqrt(squares.length);

        const x = lastMoveLocation.row;
        const y = lastMoveLocation.col;
        const lastPlayer = squares[x*size + y];
        if (lastPlayer === null)
            return null;

        var lines = {row: [], col: [], diag: [], antidiag: []};
        
        for (let i=0; i<size;i++)
        {
            lines.row.push(x*size+i)
        }

        for (let i=0; i<size;i++)
        {
            lines.col.push(i*size+y)
        }

        // last move might not be on diagonal, but checking wont hurt
        for (let i=0; i<size;i++)
        {
            lines.diag.push(i*size+i)
        }
        const reducer = (accumulator, currentValue) => accumulator && (squares[currentValue] === lastPlayer)
        // anti-diagonal
        for (let i=0; i<size;i++)
        {
            lines.antidiag.push(i*size+size-i-1)
        }

        for (let lineName in lines){
            const line = lines[lineName];
            const result = line.reduce(reducer, true)
            if (result)
            {
                return squares[line[0]];
            }
        }
        for (let i=0; i<squares.length; i++){
            if (squares[i] === null)
            {
                return null
            }
        }
        return 'T';
    }


    renderBoard(i)
    {
        return (
            <Board key={i}
                size={this.props.size}
                squares={this.state.squares[i]}
                winner={this.state.localWinners[i]}
                clickable={this.isBoardValid(i)}
                onClick={(p) => {this.handleClick(p, i)}}
            />
        );
    }

    render()
    {
      const grid = generateGridNxN(
        'game', this.props.size, this.renderBoard);
        return (
          <div className="game-container">
              {grid}
          </div>
      );
    }

}

