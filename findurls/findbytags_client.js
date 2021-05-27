import React from 'react'
import { API } from 'aws-amplify';

class FindByTagsComp extends React.Component {
    constructor(props) {
        super(props);
        this.state = { value: '' }

        this.findbytags_style = {
            marginTop: '20px',
            marginBottom: '20px'
        }
    }

    // change the value by user input
    handleChange = (e) => {
        console.log('inputEvent', e.target.value)
        this.setState({ value: e.target.value })
    }

    // separate and encoded by base64
    handleTagList = (input) => {
        this.newInput = input.split(',')
        return this.newInput;
        // return btoa(this.newInput); <- this is for base64 encoded
    };


    handleSubmit = (e) => {
        const apiName = 'fit5225web';
        const path = '/find-by-tags';
        const myInit = {
            body: { tags: this.handleTagList(this.state.value) }, // might need some test
            headers: {
            },
        };

        API
            .post(apiName, path, myInit)
            .then(response => {
                alert('Relevant urls: ' + response.body.links);  // <- might be need some test
                console.log(response.status);
            })
            .catch(error => {
                console.log(error.response);
            });

    }
    render() {
        return (
            <React.Fragment>
                <div style={this.findbytags_style}>
                    <h2> Find By Tags </h2>
                    <p> Please use ',' to separate different tags 'cat,dog,ball' </p>
                    <form onSubmit={this.handleSubmit}>
                        <input type="text" placeholder="Tags input"
                            value={this.state.value} onChange={this.handleChange} />
                        <button type="submit" >Submit</button>
                    </form>
                </div>
            </React.Fragment >
        )
    }
}

export default App
