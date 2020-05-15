import React from "react"
import {LoginForm} from "./LoginForm";
import {SignupForm} from "./SignupForm";

export class UserPopUp extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
          username: '',
          content: 'login'
      };
      this.notify_login = this.notify_login.bind(this);
      this.notify_signup = this.notify_signup.bind(this);
      this.change_content = this.change_content.bind(this)
  }

  notify_login(username) {
      this.props.notify_logged(username);
      this.setState({username: username, content: "logged in"});
      console.log("hi");
  }
  notify_signup(username) {
      this.props.notify_logged(username);
      this.setState({username: username, content: "signed up"});
  }

  change_content(c) {
      this.setState({content: c});
  }

  render() {
      console.log(this.state.content);
      switch(this.state.content) {
          case "login":
              return <LoginForm notify_login={this.notify_login} change_content={this.change_content}/>;
          case "signup":
              return <SignupForm notify_signup={this.notify_signup} change_content={this.change_content}/>;
          case "logged in":
              return <h1>Hello {this.state.username}</h1>;
          case "signed up":
              return (
                  <div>
                      <h1>Hello {this.state.username}</h1>
                      <h4>A confirmation email have been sent to you. Please confirm your email.</h4>
                  </div>);
      }
  }
}