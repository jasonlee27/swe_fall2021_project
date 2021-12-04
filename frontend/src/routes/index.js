import React, {Component} from 'react';
import { Switch, Route } from 'react-router-dom';
import axios from 'axios';
import Home from './home';
import Account from './account';

class Main extends Component {
    constructor(props) {
        super(props);

        //--- if reload page set Authorization header ----
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + sessionStorage.getItem('token');
    }

    render() {
        return (
            <Switch>
                <Route exact path='/' component={Home}/>
                <Route exact path='/account' component={Account}/>
            </Switch>
        )
    }
}


export default Main;
