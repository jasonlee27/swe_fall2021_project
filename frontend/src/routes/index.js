import React, {Component} from 'react';
import { Switch, Route } from 'react-router-dom';
import axios from 'axios';
import Home from './home';

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
            </Switch>
        )
    }
}


export default Main;
