import React from 'react';

export class PythonField extends React.Component {
    render() {
        return <div>
            <text>Python code:</text>
            <div style={{border: '2px solid black', height: 500, overflow: 'auto'}}>
                <ol>
                    {this.props.commands.map((command) => <li>{command}</li>)}
                </ol>
            </div>
        </div>
    }
}