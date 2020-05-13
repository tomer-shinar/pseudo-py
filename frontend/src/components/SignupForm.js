import React from 'react';
import PropTypes from 'prop-types';

export class SignupForm extends React.Component {

  constructor(props) {
        super(props);
        this.state = {
            username: '',
            email: '',
            password: ''
        };
        this.handle_change = this.handle_change.bind(this);
    }

  handle_change(e) {
    const target = e.target;
    const value = target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  render() {
      return (
          <div>
              <form onSubmit={e => this.props.handle_signup(e, this.state)}>
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
                <input type="submit" />
              </form>
          </div>

    );
  }
}


SignupForm.propTypes = {
  handle_signup: PropTypes.func.isRequired
};

//todo I am not a robot
//todo confirm password
//todo email verification