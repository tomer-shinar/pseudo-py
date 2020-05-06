import React from 'react';

export class PseudoField extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: ''
    };

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
    this.props.onChange(event);
  }

  render() {
    return (
      <div>
        <h3>
          Pseudo code:
        </h3>
        <textarea value={this.state.value} onChange={this.handleChange} style={{width:'50%', resize: "none"}}
                  rows="30"/>
      </div>
    );
  }
}