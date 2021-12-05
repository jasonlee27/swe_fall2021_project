import React, {Component} from 'react';
import { Switch, Route } from 'react-router-dom';
import axios from 'axios';
import Home from './home';
import Account from './account';
import ProductPage from './productPage';
import Password from './password';
import Location from './location';

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
                <Route exact path='/productpage' component={ProductPage}/>
                <Route exact path='/account' component={Account}/>
                <Route exact path='/location' component={Location}/>
                <Route exact path='/password' component={Password}/>
            </Switch>
        )
    }
}


export default Main;
