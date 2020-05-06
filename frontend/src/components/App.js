import React, { Component } from "react";
import { render } from "react-dom";
import {TranslateScreen} from "./TranslateScreen";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  /**componentDidMount() {
    fetch("api/lead")
      .then(response => {
        if (response.status > 400) {
          return this.setState(() => {
            return { placeholder: "Something went wrong!" };
          });
        }
        return response.json();
      })
      .then(data => {
        this.setState(() => {
          return {
            data,
            loaded: true
          };
        });
      });
  }**/

  render() {
    return (
        <TranslateScreen />
    );
  }
}

export default App;

const container = document.getElementById("app");
render(<App />, container);