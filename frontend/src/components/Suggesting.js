import React from "react"
import axios from "axios";

export class Suggesting extends React.Component {
    constructor(props) {
        super(props);
        let translation = this.props.translation.filter(function(item) {
            return !(item[0] === "");
        });
        this.state = {
            fields: translation.map((item) => {
                return {
                    pseudo: item[0],
                    python: item[1],
                };
            })
        };
        this.handle_change = this.handle_change.bind(this);
        this.handle_suggest = this.handle_suggest.bind(this);
        this.handle_cancel = this.handle_cancel.bind(this);
    }

    /**
     * set the change the python of the changing field
     * @param e the event
     * @param at_index the index of the field
     */
    handle_change(e, at_index) {
        e.preventDefault()
        console.log(at_index);
        this.setState({fields: this.state.fields.map((item, index) => {
            return index === at_index ? {
                pseudo: item.pseudo,
                python: e.target.value
            } : item;
            })});
    }

    handle_cancel() {
        console.log("cancel");
        this.props.notify_cancel();
    }

    handle_suggest(event) {
        event.preventDefault();
        axios({
            url: '/suggest/',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `JWT ${localStorage.getItem('token')}`
            },
            data: {
                origin: this.props.translation,
                suggestion: this.state.fields.map(value=>[value.pseudo, value.python])
            }
        })
            .then(response => {
                this.props.notify_suggested();
            })
            .catch(error => {
                if (error.response.status === 403)
                    this.props.notify_message(error.response.data);
                if (error.response.status === 401)
                    this.props.notify_message("It's been a while since you logged in, please sign out and log in again");
            });
    }

    render() {
        return (
            <div>
                <h1>
                    Suggest a new translation
                </h1>
                <form>
                    <ol>
                        {this.state.fields.map((field, index) => {
                            return <li>
                                <label>
                                    <h4>{this.state.fields[index].pseudo}</h4>
                                    <textarea
                                        value={this.state.fields[index].python}
                                        onChange={e => this.handle_change(e, index)}
                                        style={{width:'70%', resize: "none", border: '2px solid black'}}
                                        rows="3"
                                    />
                                </label>
                            </li>
                        })}
                    </ol>
                </form>
                <div style={{display: "flex", justifyContent: "center", alignItems: "center"}}>
                    <button onClick={this.handle_suggest} title="Suggest"
                        style={{width: 300, height: 100, paddingLef: 500, backgroundColor: "#00be00"}}>
                        <div style={{ fontSize: 40 }}>Suggest</div>
                    </button>
                    <p style={{ fontSize: 35 }} onClick={this.handle_cancel}>cancel</p>
                </div>
            </div>
        )
    }
}