import React from 'react'
import { API } from 'aws-amplify';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = { url: '', tags:''}  

        this.addTags_style = {
            marginTop: '20px',
            marginBottom: '20px'
        }
    }

    // change the value by user input
    handleChange = (e) => {
        console.log('inputEvent', e.target.value)
        this.setState({ url: e.target.value, tags: this.state.tags })
        
    }

    handleChange2 = (e) => {
      console.log('inputEvent', e.target.value)
      this.setState({url: this.state.url, tags: e.target.value }) 
  }


    handleTagList = (input) => {
        this.newInput = input.split(',')
        return this.newInput;

    };


    handleSubmit = (e) => {
        const apiName = 'fit5225web';
        const path = '/add-delete';
        const myInit = {
        body: { url: this.state.url}, // might need some test
             headers: {
             },
         };
         alert('url: ' + this.state.url + ',tags: '+ this.state.tags);

        API
            .post(apiName, path, myInit)
            .then(response => {
                alert('Relevant urls: ' + response.body.status); // <- might be need some test
                console.log(response.status); 
            })
            .catch(error => {
                console.log(error.response);
            });

    }
    render() {
        return (
            <React.Fragment>
                <div style={this.addTags_style}>
                    <h2> Add Tags</h2>

                    <form onSubmit={this.handleSubmit}> 
                      <div>
                      <textarea cols="30" rows="5" placeholder="add url"
                        value={this.state.url} onChange={this.handleChange} /> 
                      </div>
                      <div>
                      <textarea cols="30" rows="1" type="text" placeholder="Tags input"
                        value={this.state.tags} onChange={this.handleChange2} /> 
                      </div>

                      <button type="submit" >Submit</button>
                    </form>
                </div>
            </React.Fragment >
        )
    }
}

export default App


