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
            <div style={{display: "flex", justifyContent: "center", alignItems: "center", paddingTop:50}}>
                {this.props.display_buttons && (
                    <div>
                        <img src={"/static/frontend/X.jpg"} height="100" alt="" onClick={this.props.handle_suggest}/>
                        <p>suggest new Translation</p>
                    </div>
                )}
                <button onClick={this.handleTranslate} title="Translate"
                        style={{width: 300, height: 100, paddingLef: 500, backgroundColor: "#00be00"}}>
                    <div style={{ fontSize: 40 }}>Translate</div>
                </button>
                {this.props.display_buttons && (
                    <div>
                        <img src={"/static/frontend/V.png"} height="100" alt="" onClick={this.props.handle_up_vote}/>
                        <p>Thanks</p>
                    </div>
                )}
            </div>
        </div>);
    }
}