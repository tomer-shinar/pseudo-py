import React from 'react';
import Loader from 'react-loader-spinner';


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
                {this.props.display_spinner &&
                <div style={{display: "flex", alignItems: "center", justifyContent: "center"}}>
                    <Loader type="BallTriangle" color="#00FF00" height={80} width={80} />
                </div>}
            </div>
        </div>
    }
}