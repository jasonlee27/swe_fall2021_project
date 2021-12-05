import React, {Component} from 'react'
import Button from '../../components/button'

class Location extends Component {
    constructor(props) {
        super(props);
        this.reset = this.reset.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.state = {
            location: '',
        }
    }

    handleChange(event) {
      this.setState({location: event.target.value});
    }

    reset() {
        alert(this.state.location)
    }

    render() {
        const location = this.state;
        return (
            <div>
                <div className="container">
                    <div className="starter-template">
                        <div className="row">
                            <div className="col-md-12">
                                <div className="product-header">
                                    <h2><strong>Location Reset</strong></h2>
                                </div>
                            </div>
                            <div className="col-md-12">
                            <div className="form-horizontal" onSubmit={this.passwordReset}>
                                <div className="form-group">

                                    <div className="col-sm-8">
                                    <label className="col-sm-3 control-label">
                                        New Location
                                        <select value={this.state.value} onChange={this.handleChange}>
                                          <option value="location 1">Location 1</option>
                                          <option value="location 2">Location 2</option>
                                          <option value="location 3">Location 3</option>
                                          <option value="location 4">Location 4</option>
                                        </select>
                                    </label>
                                    </div>
                                </div>
                                <Button onClick={this.reset}>Set</Button>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Location;