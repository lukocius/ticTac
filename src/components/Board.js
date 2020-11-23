import React, { Component} from "react";
import Square from "./Square";


// Helper function. TODO move to separate file?
// generatorFunction makes it so that in can be used for ž
// nested grids (NxNxBxB  for example).
export function generateGridNxN(className, size, generatorFunction)
{
    var rows = [];
    for (let i = 0; i < size; i++)
    {
        let cols = [];
        for (let j = 0; j < size; j++)
        {
            cols.push(generatorFunction(i*size + j));
        }
        rows.push(
            <div className={className+'-row'} key={i}>{cols}</div>
        );
    }
    return (
        <div className={className}>{rows}</div>
    );
}

export default class Board extends Component
{
    constructor(props)
    {
        super(props);
        this.renderSquare = this.renderSquare.bind(this);
    }

    renderSquare (i)  // give index to the square.
    {
        return (
            <Square key={i}
                value={this.props.squares[i]}
                winner={this.props.winner}
                clickable={this.props.clickable}
                onClick={() => this.props.onClick(i)}
            />
        )
    }

    render()
    {
        if (this.props.winner)
        {
            return (
                <Square key={0}
                value={this.props.winner}
                winner={this.props.winner}
                size={this.props.size}
            />
            )
        }
        return generateGridNxN(
            'board',
            this.props.size,
            this.renderSquare
        );
    }
}