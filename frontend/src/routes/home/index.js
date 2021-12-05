import React, {Component} from 'react'
import Button from '../../components/button'

class Home extends Component {
    constructor(props) {
        super(props);
        this.goToProductPage = this.goToProductPage.bind(this);
        this.goToPasswordPage = this.goToPasswordPage.bind(this);
        this.goToLocationPage = this.goToLocationPage.bind(this);
    }

    goToProductPage() {
        this.props.history.push('/productpage');
    }
    
    goToPasswordPage() {
        this.props.history.push('/password');
    }
    
    goToLocationPage() {
        this.props.history.push('/location');
    }

    render() {
        return (
            <div>
                <div className="container">
                    <div className="starter-template">
                        <div className="row">
                            <div className="col-md-12">
                                <div className="product-header">
                                    <h2><strong>Home</strong></h2>
                                </div>
                            </div>
                            <div className="col-md-12">
                                <Button onClick={this.goToProductPage}>Start Shopping</Button>
                                <Button onClick={this.goToPasswordPage}>Update password</Button>
                                <Button onClick={this.goToLocationPage}>Change Location</Button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Home;