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
      <div  style={{width: "95%", paddingLeft: 50, paddingRight:50}}>
        <h3 style={{paddingLeft: 10}}>
          Pseudo code:
        </h3>
        <textarea value={this.state.value} onChange={this.handleChange} style={{width:'100%', resize: "none",
          border: '2px solid black'}}
                  rows="35"/>
      </div>
    );
  }
}