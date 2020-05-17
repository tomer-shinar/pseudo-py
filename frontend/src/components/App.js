import React, { Component } from 'react';
import { render } from "react-dom";
import {Header} from "./Header";
import {Content} from "./Content";
import axios from "axios";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      logged_in: false,
    };
    this.notify_log = this.notify_log.bind(this);
  }

  notify_log(logged, username, password) {
    this.setState({logged_in: logged, username:username, password:password});
  }


  render() {
    return (
        <span>
          <Header notify_log={this.notify_log} name="header"/>
          <Content is_logged_in={this.state.logged_in}/>
        </span>
    )
  }
}


const container = document.getElementById("app");
render(<App />, container);