import React from "react";
import axios from "axios";
import {translateUrl} from "../constants";
import {PseudoField} from "./pseudoField";
import {PythonField} from "./pythonField";
import { trackPromise } from 'react-promise-tracker';


export class TranslateScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            pseudo: "",
            translation: [[]],
            currentlyTranslating: false
        };
        this.handleTranslate = this.handleTranslate.bind(this);
        this.handleChange = this.handleChange.bind(this);
    }
    handleChange(e) {
        this.setState({pseudo: e.target.value});
    }

    handleTranslate(e) {
        /**
         * handle the event of clicking translate
         */
        this.setState({currentlyTranslating: true});
        e.preventDefault();
        this.setState({currentlyTranslating: true});
        axios.post(translateUrl, {"pseudo": this.state.pseudo})
         .then((response) => {
            this.setState({translation: JSON.parse(response.data), currentlyTranslating: false});
            this.props.notify_translation(this.state.translation);
        }).catch(error => {
            this.setState({currentlyTranslating: false});
        });
    }
    render() {
        return (
        <div>
            <div style={{display:'flex'}}>
                <PseudoField onChange={this.handleChange}/>
                <PythonField display_spinner={this.state.currentlyTranslating} commands={this.state.translation.map((tuple)=>tuple[1])}/>
            </div>
            <div style={{display: "flex", justifyContent: "center", alignItems: "center", paddingTop:20}}>
                {this.props.display_buttons && (
                    <div style={{paddingRight: 100}}>
                        <img src={"/static/frontend/X.png"} height="90" alt="" onClick={this.props.handle_suggest}/>
                        <p style={{justifyContent: "center", alignItems: "center"}}>suggest new Translation</p>
                    </div>
                )}
                <button onClick={this.handleTranslate} title="Translate"
                        style={{width: 300, height: 100, backgroundColor: "#00be00"}}>
                    <div style={{ fontSize: 40 }}>Translate</div>
                </button>
                {this.props.display_buttons && (
                    <div style={{paddingLeft: 100}}>
                        <img src={"/static/frontend/V.jpeg"} height="90" alt="" onClick={this.props.handle_up_vote}/>
                        <p style={{justifyContent: "center", alignItems: "center"}}>Thanks</p>
                    </div>
                )}
            </div>
        </div>);
    }
}