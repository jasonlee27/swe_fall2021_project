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
                                          <option value="location 1">2112 preston road, dallas</option>
                                          <option value="location 2">233 frankford road, Richardson</option>
                                          <option value="location 3">1817 london bridge, London</option>
                                          <option value="location 4">1221 walnut road, seattle</option>
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