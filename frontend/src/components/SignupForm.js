import React from 'react';
import axios from "axios";

export class SignupForm extends React.Component {

  constructor(props) {
        super(props);
        this.state = {
            username: '',
            email: '',
            password: '',
            err_mess: ''
        };
        this.handle_change = this.handle_change.bind(this);
        this.handle_signup = this.handle_signup.bind(this);
    }

  handle_change(e) {
    const target = e.target;
    const value = target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  handle_signup(e) {
    e.preventDefault();
      let data = {
          username: this.state.username,
          password: this.state.password,
          email: this.state.email
      };
    axios({
        url: '/users/',
        method: 'POST',
        headers: {
        'Content-Type': 'application/json',
        },
        data: data
    })
        .then(response => {
            localStorage.setItem('token', response.data.token);
            this.props.notify_signup(this.state.username);
        })
        .catch(error => {
            console.log(JSON.stringify(error.response.data));
            this.setState({err_mess: error.response.data});
        });
  }

  render() {
      return (
          <div>
              <form onSubmit={this.handle_signup}>
                <h4>Sign Up</h4>
                <label htmlFor="username">Username</label>
                <input
                  type="text"
                  name="username"
                  value={this.state.username}
                  onChange={this.handle_change}
                />
                <label htmlFor="email">email</label>
                <input
                  type="text"
                  name="email"
                  value={this.state.email}
                  onChange={this.handle_change}
                />
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  name="password"
                  value={this.state.password}
                  onChange={this.handle_change}
                />
                <input type="submit" value="Submit" />
              </form>
              <p color={'#FF0000'}>{this.state.err_mess}</p>
              <p onClick={e=>{this.props.change_content("login")}}>
                Have a user?
                log in!
            </p>
          </div>

    );
  }
}


//todo I am not a robot
//todo confirm password
//todo email verification