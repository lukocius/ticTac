import React from "react";

export default function Square(props) {
    var style = {};
    if (props.value){  // X and O will have different colors
        style.color = props.value === 'X' ? '#fc7341' : '#2db2e2';
    }

    if (props.winner)  // Square is in completed sub-board.
    {
        style.fontSize = props.size*24;
        style.width = props.size*(34-1)-1;
        style.height = style.width;
        if (props.winner === 'X'){
            style.background = '#ffccb5';
        }

        else if (props.winner === 'O'){  // TODO Draw is possible.
            style.background = '#dbf5ff';
        }

        else {
            style.background = '#e2ffec';
        }

        return (
            <div className='board'>
            <div className='board-complete' style={style}>
                {props.winner}
            </div>
            </div>
        )
    }
    if (props.clickable){
        style.background= '#109910';
    }

    return (
    <button className="square" style={style} onClick={props.onClick}>
        {props.value}
    </button>   
    ); 
}
