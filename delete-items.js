import React from 'react'

// import { API } from 'aws-amplify';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = { value: '' }  //object -> this.state.value (user de value)
        

        this.deleteItems_style = {
            marginTop: '20px',
            marginBottom: '20px'
        }
    }

    // change the value by user input
    handleChange = (e) => {
        console.log('inputEvent', e.target.value)
        this.setState({ value: e.target.value }) 
    }

    handleTagList = (input) => {
        this.newInput = input.split(',')
        return this.newInput;
    };


    handleSubmit = (e) => {
        //alert('Tags input: ' + this.handleTagList(this.state.value)); 
         const apiName = 'fit5225web';
         const path = '/add-delete';
        const myInit = {
        body: { urls: this.state.value}, // might need some test
             headers: {
             },
         };
         alert('Delete successfully: ' + this.state.value);

        API
            .delete(apiName, path, myInit)
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
                <div style={this.deleteItems_style}>
                    <h2> Delete</h2>
                    <p> test </p>
                    <form onSubmit={this.handleSubmit}> 
                        <input type="text" placeholder="Delete"
                            value={this.state.value} onChange={this.handleChange} /> 
                        <button type="submit" >Submit</button>
                    </form>
                </div>
            </React.Fragment >
        )
    }
}

export default App
