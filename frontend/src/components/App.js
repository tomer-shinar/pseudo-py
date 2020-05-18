import React, { Component } from 'react';
import { render } from "react-dom";
import {Header} from "./Header";
import {Content} from "./Content";
import { usePromiseTracker } from "react-promise-tracker";
import Loader from 'react-loader-spinner';

// the loading spinner appears while loading
const LoadingIndicator = props => {
  const { promiseInProgress } = usePromiseTracker();
  return (
      promiseInProgress &&
      <div
      style={{
        width: "100%",
        height: "100",
        display: "flex",
        justifyContent: "center",
        alignItems: "center"
      }}
    >
      <Loader type="ThreeDots" color="#2BAD60" height="100" width="100" />
    </div>
  );
};

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