import React from 'react';
import Game from './components/Game.js';

export default class App extends React.Component
{
    render()
    {
        return (
            <div className="app">
                <Game key={0}
                    size={3}
                />
            </div>
        );
    }
}