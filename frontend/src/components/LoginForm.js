import React from 'react';
import PropTypes from 'prop-types';

export class LoginForm extends React.Component {
  constructor(props) {
        super(props);
        this.state = {
            username: '',
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
      <form onSubmit={e => this.props.handle_login(e, this.state)}>
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
        <input type="submit" />
      </form>
    );
  }
}


LoginForm.propTypes = {
  handle_login: PropTypes.func.isRequired
};