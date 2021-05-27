import React from 'react'
import { API } from 'aws-amplify';

class FindByImageComp extends React.Component {

    constructor(props) {
        super(props);

        this.findbyimage_style = {
            marginTop: '20px',
            marginBottom: '20px'
        }
    }

    onChange = (e) => {
        console.log("file to upload:", e.target.files[0])
        this.file = e.target.files[0]

        if (this.file) {
            const reader = new FileReader();
            reader.onload = this._handleReaderLoaded.bind(this)
            reader.readAsBinaryString(this.file)
        }
    }

    _handleReaderLoaded = (readerEvt) => {
        let binaryString = readerEvt.target.result
        this.setState({
            base64TextString: btoa(binaryString)
        })
    }

    onFileSubmit = (e) => {
        e.preventDefault()
        //console.log("binary string:", this.state.base64TextString)
        console.log("binary string:", this.file.name)
        const apiName = 'fit5225web'; // replace this with your api name.
        const path = '/find-by-image'; //replace this with the path you have configured on your API
        const myInit = {
            body: { name: this.file.name, file: this.state.base64TextString }, // replace this with attributes you need
            headers: {
            }, // OPTIONAL
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
                <div style={this.findbyimage_style}>
                    <h2> Find by image </h2>
                    <p> Please submit the file to search relevant image urls</p>
                    <form onSubmit={(e) => this.onFileSubmit(e)} onChange={(e) => this.onChange(e)}>
                        <input type="file" name="image" id="file" accept=".jpeg, .png, .jpg" />

                        <input type="submit" />
                    </form>
                </div>
            </React.Fragment>
        )
    }
}
export default UploadComp