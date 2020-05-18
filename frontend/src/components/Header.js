import React from "react";
import Popup from "reactjs-popup";
import {UserPopUp} from "./UserPopUp";
import axios from "axios";

/**
 * class for the header contains the logo and log in / sign out option
 */
export class Header extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            logged_in: !!localStorage.getItem('token'),
            username: '',
        };
        this.notify_logged = this.notify_logged.bind(this);
        this.handle_logout = this.handle_logout.bind(this);
    }

    componentDidMount() {
    if (this.state.logged_in) {
      fetch('current_user/', {
        headers: {
          Authorization: `JWT ${localStorage.getItem('token')}`
        }
      })
        .then(res => {
            if (!res.ok)
                throw new Error();
            return res.json();
        })
        .then(json => {
          this.setState({ username: json.username});
          this.props.notify_log(true, json.username, json.password);
        })
         .catch(error =>{
             this.handle_logout()
         });
    }
  }


    notify_logged(username, password) {
        this.props.notify_log(true, username, password);
        this.setState({logged_in: true, username:username});
    }

    handle_logout() {
        localStorage.removeItem('token');
        this.props.notify_log(false, "", "");
        this.setState({logged_in: false, username: ""})
    }

    render() {
        let user_option;
        if (this.state.logged_in) {
            user_option = (
                <div>
                    <p>Hello {this.state.username}</p>
                    <p onClick={this.handle_logout}>sign out</p>
                </div>
            );
        } else {
            user_option = (
                <Popup
                    trigger={<p> login </p>}
                    modal
                    closeOnDocumentClick>
                    {close => (
                        <div className="modal">
                            <a className="close" onClick={close}>
                                &times;
                            </a>
                            <UserPopUp notify_logged={this.notify_logged}/>
                        </div>
                    )}
                </Popup>
            );
        }
        return (
            <div style={{backgroundColor: '#26d00b', display: 'flex', alignItems: "center"}}>
                <img src={"/static/frontend/logo.png"} width="600" height="125" alt=""
                     style={{paddingLeft: 200, paddingRight: 100}}/>
                {this.state.logged_in && <div>
                    <p>Hello {this.state.username}</p>
                    <p onClick={this.handle_logout}>sign out</p>
                </div>}
                <Popup
                    trigger={<p> {this.state.logged_in? "": "login"} </p>}
                    modal
                    closeOnDocumentClick>
                    {close => (
                        <div className="modal">
                            <a className="close" onClick={close}>
                                &times;
                            </a>
                            <UserPopUp notify_logged={this.notify_logged}/>
                        </div>
                    )}
                </Popup>
            </div>
        )
    }
}