import React from "react"
import {TranslateScreen} from "./TranslateScreen";
import {Suggesting} from "./Suggesting";
import axios from "axios";

/**
 * class of the content displayed on the screen.
 * contains the translation screen and suggestion
 */
export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            last_translation: [],
            screen: "translate", // translate or suggest
            last_action: "", // "" or translated
            message: ""
        };
        this.notify_message = this.notify_message.bind(this);
        this.notify_suggested = this.notify_suggested.bind(this);
        this.notify_translation = this.notify_translation.bind(this);
        this.handle_up_vote = this.handle_up_vote.bind(this);
        this.handle_suggest = this.handle_suggest.bind(this);
        this.notify_cancel = this.notify_cancel.bind(this);
    }

    notify_translation(translation) {
        this.setState({last_translation:translation, last_action:"translated", message: ""});
        console.log(JSON.stringify(translation));
    }

    notify_cancel() {
        this.setState({
            screen: "translate",
            message: ""
        });
    }

    handle_suggest(event) {
        //user requested to up vote
        event.preventDefault();
        if (this.props.is_logged_in) {
            this.setState({screen: "suggest", message: ""});
        } else {
            this.setState({message: "Please log in to suggest a new translation"});
        }

    }

    handle_up_vote(event) {
        event.preventDefault();
        if (!this.props.is_logged_in) {
            this.setState({message: "please log in to up vote"});
            return;
        }
        axios({
            url: '/upvote/',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `JWT ${localStorage.getItem('token')}`
            },
            data: {translation: this.state.last_translation}
        })
            .then(response => {
                this.setState({last_action: "", message: "Thank you for up voting"})
            })
            .catch(error => {
                if (error.response.status === 403)
                    this.notify_message(error.response.data);
                if (error.response.status === 401)
                    this.notify_message("It''s been a while since you logged in, please sign out and log in again");
            });
    }

    notify_suggested() {
        this.setState({
            screen: "translate",
            message: "Thank you for suggesting a new translation",
            last_action: ""
        });
    }

    notify_message(message) {
        this.setState({message: message})
    }


    render() {
        let screen;
        if (this.state.screen === "translate") {
            screen = <TranslateScreen
                notify_translation={this.notify_translation}
                handle_suggest={this.handle_suggest}
                handle_up_vote={this.handle_up_vote}
                display_buttons={this.state.last_action==="translated"}
            />;
        } else {
            screen = <Suggesting
                notify_suggested={this.notify_suggested}
                notify_message={this.notify_message}
                translation={this.state.last_translation}
                notify_cancel={this.notify_cancel}
            />
        }
        return <div>
            {screen}
            <div style={{justifyContent: "center", alignItems: "center", display:"flex"}} >{this.state.message}</div>
        </div>
    }
}