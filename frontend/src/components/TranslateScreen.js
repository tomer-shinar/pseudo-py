import React from "react";
import axios from "axios";
import {translateUrl} from "../constants";
import {PseudoField} from "./pseudoField";
import {PythonField} from "./pythonField";


export class TranslateScreen extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            pseudo: "",
            translation: [],
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
        axios.post(translateUrl, {"pseudo": this.state.pseudo}).then((response) => {
            this.setState({translation: response.data, currentlyTranslating: false});
        });
    }
    render() {
        return (
        <div>
            <div style={{float:'left'}}>
                <PseudoField onChange={this.handleChange}/>
                <PythonField commands={this.state.translation.map((tuple)=>tuple[0])}/>
            </div>
            <button onClick={this.handleTranslate} title="Translate"/>
        </div>);
    }
}