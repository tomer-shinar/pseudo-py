import React from 'react';
import axios from "axios";

export class LoginForm extends React.Component {
  constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            been_failed: false
        };
        this.handle_change = this.handle_change.bind(this);
        this.handle_login = this.handle_login.bind(this);
    }

  handle_change(e) {
    const target = e.target;
    const value = target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  handle_login(e) {
    e.preventDefault();
    axios( {
        url: '/token-auth/',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        data: JSON.stringify({username: this.state.username, password: this.state.password})
    })
      .then(response => {
          localStorage.setItem('token', response.data.token);
          this.props.notify_login(this.state.username)
      })
      .catch(error => {
          this.setState({been_failed: true})
      });
  }

  render() {
    return (
        <div>
            <form onSubmit={this.handle_login}>
                <h4>Log In</h4>
                <label htmlFor="username">Username</label>
                <input
                  type="text"
                  name="username"
                  value={this.state.username}
                  onChange={this.handle_change}
                />
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  name="password"
                  value={this.state.password}
                  onChange={this.handle_change}
                />
                <input type="submit" value="Submit"/>
            </form>
            <p>{this.state.been_failed ? "wrong password or username": ""}</p>
            <p onClick={e=>{this.props.change_content("signup")}}>
                Don't have a user?
                sign up!
            </p>
        </div>

    );
  }
}
