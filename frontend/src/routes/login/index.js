import React, {Component} from 'react';
import Modal from "react-bootstrap/lib/Modal";
import {ToastNotification} from '../../components/notification/ToastNotification';
import {errorMsg, successMsg, warnMsg} from '../../components/notification/ToastNotification';
import axios from 'axios';
import api from '../../api'

class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            login: {
                username: '',
                password: '',
            },
            registration: {
                userName: '',
                password: '',
                email: ''
            },
            products: '',
            openDlgFlg: false
        }
    }

    login = (e) => {
        e.preventDefault();
        let self = this;
        var bodyFormData = new FormData();
        bodyFormData.append('username', this.state.login.username);
        bodyFormData.append('password', this.state.login.password);
        //self.props.history.push('/');
        api.post('/api/login', bodyFormData)
            .then(function (response) {
                if(response.data.code == 200) {
                    //---set Authorization header ---
                    axios.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.token;
                    //token store in session storage
                    sessionStorage.setItem('token', response.data.token);
                    self.props.history.push('/');
                } else {
                    errorMsg(response.data.msg);
                    self.props.history.push('/login');
                }
            })
            .catch(function (error) {
                errorMsg('Issue with the internal system');
                console.log("login error response :: ", error);
            });
    };

    userRegistration = (e) => {
        console.log(this.state.registration);
        e.preventDefault();
        let self = this;
        var bodyFormData = new FormData();
        bodyFormData.append('username', this.state.registration.userName);
        bodyFormData.append('email', this.state.registration.email);
        bodyFormData.append('password', this.state.registration.password);
        api.post('/api/register', bodyFormData)
            .then(function (response) {
                if (response.data.code === 400)
                    warnMsg(response.data.msg);
                else
                    console.log('user registration success response :: ', response);
                    successMsg(response.data.msg);
                    self.setEmptyRegistrationState();
                    self.handleDlgClose();
                    self.props.history.push('/login');
            })
            .catch(function (error) {
                console.log("user registration error response  :: ", JSON.stringify(error));
                errorMsg(error)
            });
    };

    setEmptyRegistrationState() {
        const {registration} = this.state;
        registration.userName = '';
        registration.password = '';
        this.setState({registration});
    }

    // --------- Dialog open/close--------
    handleDlgClose() {
        this.setState({openDlgFlg: false});
    };

    handleDlgShow() {
        this.setState({openDlgFlg: true});
    };


    render() {
        const {login, registration, openDlgFlg} = this.state;
        return (
            <div className="login-container">
                <div className="starter-template">

                    <form className="form-horizontal" onSubmit={this.login}>
                        <div className="form-group">
                            <div className="col-sm-offset-5 col-sm-7">
                                <h3>Login</h3>
                            </div>
                        </div>
                        <div className="form-group">
                            <label className="col-sm-3 control-label">Username </label>

                            <div className="col-sm-8">
                                <input type="text" className="form-control" id="username" name="username"
                                       placeholder="Username"
                                       value={login.username}
                                       onChange={(e) => this.setState({
                                           login: {
                                               ...login,
                                               username: e.target.value
                                           }
                                       })}
                                       required="true"/>
                            </div>
                        </div>


                        <div className="form-group">
                            <label className="col-sm-3 control-label">Password</label>

                            <div className="col-sm-8">
                                <input type="password" className="form-control" id="password" name="password"
                                       value={login.password}
                                       onChange={(e) => this.setState({
                                           login: {
                                               ...login,
                                               password: e.target.value
                                           }
                                       })}
                                       placeholder="Password"
                                       required="true"/>
                            </div>
                        </div>
                        <div className="form-group">
                            <div className="col-sm-offset-5 col-sm-7">
                                <button type="submit" className="btn btn-primary">Login</button>
                            </div>
                        </div>
                    </form>
                    <div className="form-group req-link">
                        <a href="#" onClick={() => this.handleDlgShow()}>User Registration</a>
                    </div>
                </div>

                <Modal
                    show={openDlgFlg}
                    onHide={() => this.handleDlgClose()}
                    aria-labelledby="ModalHeader"
                >
                    <form onSubmit={this.userRegistration}>
                        <Modal.Header closeButton>
                            <Modal.Title id='ModalHeader'>User Registration</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>
                            <div className="form-horizontal" onSubmit={this.userRegistration}>
                                <div className="form-group">
                                    <label className="col-sm-3 control-label">Username </label>

                                    <div className="col-sm-8">
                                        <input type="text" className="form-control" id="username" name="username"
                                               placeholder="Username"
                                               maxLength="50"
                                               value={registration.userName}
                                               onChange={(e) => this.setState({
                                                   registration: {
                                                       ...registration,
                                                       userName: e.target.value
                                                   }
                                               })}
                                               required="true"/>
                                    </div>
                                </div>
                                
                                <div className="form-group">
                                    <label className="col-sm-3 control-label">Email </label>

                                    <div className="col-sm-8">
                                        <input type="text" className="form-control" id="email" name="email"
                                               placeholder="Email"
                                               maxLength="50"
                                               value={registration.email}
                                               onChange={(e) => this.setState({
                                                   registration: {
                                                       ...registration,
                                                       email: e.target.value
                                                   }
                                               })}
                                               required="true"/>
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label className="col-sm-3 control-label">Password</label>

                                    <div className="col-sm-8">
                                        <input type="password" className="form-control" id="password" name="password"
                                               value={registration.password}
                                               maxLength="50"
                                               onChange={(e) => this.setState({
                                                   registration: {
                                                       ...registration,
                                                       password: e.target.value
                                                   }
                                               })}
                                               placeholder="Password"
                                               required="true"/>
                                    </div>
                                </div>
                            </div>
                        </Modal.Body>
                        <Modal.Footer>
                            <button className='btn btn-primary' type="button" onClick={() => this.handleDlgClose()}>
                                Cancel
                            </button>
                            <button className='btn btn-primary' type="submit">
                                Registration
                            </button>
                        </Modal.Footer>
                    </form>
                </Modal>
                <ToastNotification/>
            </div>
        )
    };
}

export default Login;
