import React from 'react'
import { Link } from 'react-router-dom'

const Header = () => (
    <div className="navbar-wrapper">
        <nav className="navbar navbar-inverse navbar-static-top">
            <div className="container">
                <div className="navbar-header">
                    <button type="button" className="navbar-toggle collapsed"
                            data-toggle="collapse" data-target="#navbar"
                            aria-expanded="false" aria-controls="navbar">
                        <span className="sr-only">Toggle navigation</span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                    </button>
                    <Link className="navbar-brand" to='/'>Home</Link>
                </div>
                <div id="navbar" className="navbar-collapse collapse">
                    <ul className="nav navbar-nav">
                        <li ><Link to='/account'>Profile</Link></li>
                        <li ><Link to='/location'>Location</Link></li>
                        <li ><a href="#" onClick={() => {sessionStorage.removeItem('token'); window.location = '/login'}}>Logout</a></li>
                    </ul>
                </div>
            </div>
        </nav>
    </div>
);

export default Header;