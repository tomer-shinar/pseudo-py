import React, { Component } from 'react';
import { render } from "react-dom";
import {Header} from "./Header";
import {TranslateScreen} from "./TranslateScreen";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      logged_in: !!localStorage.getItem('token'),
    };
    this.notify_log = this.notify_log.bind(this);
  }

  notify_log(logged) {
    this.setState({logged_in: logged});
  }

  render() {
    return (
        <span>
          <Header notify_log={this.notify_log}/>
          <TranslateScreen/>
        </span>
    )
  }
}


const container = document.getElementById("app");
render(<App />, container);