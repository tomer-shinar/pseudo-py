import React from 'react';

export class PythonField extends React.Component {
    render() {
        return <div style={{paddingLeft: 50, paddingRight:50, paddingTop:2, width:"100%"}}>
            <h3 style={{paddingLeft: 10}}>
                Python code:
            </h3>
            <div style={{border: '2px solid black', height: 505, overflow: 'auto', paddingTop:20}}>
                <ol>
                    {this.props.commands.map((command) => <li>{command}</li>)}
                </ol>
            </div>
        </div>
    }
}