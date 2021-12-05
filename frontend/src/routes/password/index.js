import React, {Component} from 'react'
import Button from '../../components/button'

class Password extends Component {
    constructor(props) {
        super(props);
        this.reset = this.reset.bind(this);
        this.state = {
            password: {
                current: '',
                npassword: '',
                rpassword: '',
            }
        }
    }

    reset() {
        alert('reset')
    }

    render() {
        const password = this.state;
        return (
            <div>
                <div className="container">
                    <div className="starter-template">
                        <div className="row">
                            <div className="col-md-12">
                                <div className="product-header">
                                    <h2><strong>Password Reset</strong></h2>
                                </div>
                            </div>
                            <div className="col-md-12">
                            <div className="form-horizontal" onSubmit={this.passwordReset}>
                                <div className="form-group">
                                    <label className="col-sm-3 control-label">Current Password</label>

                                    <div className="col-sm-8">
                                        <input type="text" className="form-control" id="cpassword" name="cpassword"
                                               placeholder="Current Password"
                                               maxLength="50"
                                               value={password.current}
                                               onChange={(e) => this.setState({
                                                   password: {
                                                       ...password,
                                                       current: e.target.value
                                                   }
                                               })}
                                               required="true"/>
                                    </div>
                                </div>
                                
                                <div className="form-group">
                                    <label className="col-sm-3 control-label">New Password </label>

                                    <div className="col-sm-8">
                                        <input type="text" className="form-control" id="npassword" name="npassword"
                                               placeholder="New Password"
                                               maxLength="50"
                                               value={password.npassword}
                                               onChange={(e) => this.setState({
                                                   password: {
                                                       ...password,
                                                       npassword: e.target.value
                                                   }
                                               })}
                                               required="true"/>
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label className="col-sm-3 control-label">Retype Password</label>

                                    <div className="col-sm-8">
                                        <input type="rpassword" className="form-control" id="rpassword" name="rpassword"
                                               value={password.rpassword}
                                               maxLength="50"
                                               onChange={(e) => this.setState({
                                                   password: {
                                                       ...password,
                                                       rpassword: e.target.value
                                                   }
                                               })}
                                               placeholder="Retype Password"
                                               required="true"/>
                                    </div>
                                </div>
                                <Button onClick={this.reset}>Reset</Button>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Password;