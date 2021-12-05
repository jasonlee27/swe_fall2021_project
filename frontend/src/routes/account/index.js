import React, {Component} from 'react'
import {errorMsg, successMsg} from '../../components/notification/ToastNotification';
import api from '../../api';


class Account extends Component {
    constructor(props) {
        super(props);
        this.state = {
            profile: {
                name:'None',
                email:'None',
                payment:[],
                address: [],
            }
        };
        this.loadProfile();
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevState.current !== this.state.current) {
            this.loadProfile();
        }
    }


    loadProfile = () => {
        let self = this;
        //api.get('/api/products', { params: {page : self.state.current, limit : self.state.limit }})
        //    .then(function (response) {
        //        console.log("products success response :: ", response.data);
        //        self.setState({products: []});
        //        self.setState({products: self.state.products.concat(response.data.content)});
        //        self.setState({current: response.data.number});
        //        self.setState({totalPages: response.data.totalPages-1});
        //        self.setState({totalElements: response.data.totalElements});
        //    })
        //    .catch(function (error) {
        //        console.log("products error response :: ", error);
        //    });

        self.setState({
            profile: {
                name:'None',
                email:'None',
                payment:[],
                address: [],
            },
        });
    };

    resetPassword = (e) => {
        e.preventDefault();
        const {product} = this.state;
        let self = this;
        api.put('/api/products/'+product.id, product)
            .then(function (response) {
                console.log('product update success response :: ',response);
                successMsg('Successfully product updated.');
                self.handleUpdateDlgClose();
                self.loadProfile();
            })
            .catch(function (error) {
                console.log("product update error response :: ",error);
                errorMsg('Failed to Update product.');
            });

    };

    changeLocation = (e) => {
        e.preventDefault();
        const {product} = this.state;
        let self = this;
        api.delete('/api/product/'+product.id)
            .then(function (response) {
                console.log('product delete success response :: ',response);
                successMsg('Successfully Product Deleted.');
                self.handleDeleteDlgClose();
                self.loadProfile();
            })
            .catch(function (error) {
                console.log("product delete error response :: ",error);
                errorMsg('Failed to Delete Product.');
            });

    };

    // ---------Update Dialog open/close--------
    handleUpdateDlgClose() {
        this.setState({updateDlgFlg: false});
    };

    handleUpdateDlgShow(data) {
        this.setProfileToState(data);
        this.setState({updateDlgFlg: true});
    };

    setProfileToState(data) {
        const {profile} = this.state;
        if (data !== null) {
            profile.name = data.name;
            profile.email = data.email;
            profile.payment = data.payment;
            profile.address = data.address;
            this.setState({profile});
        }
    };

    render() {
        const profile = this.state;
        //let productItem = [];
        //for (let number = 0; number <= totalPages; number++) {
        //    productItem.push(
        //        <Pagination.Item active={number === current} onClick={() => this.onPaginationChange(number)}>{number+1}</Pagination.Item>
        //    );
        //}

        return (
            <div>
                <div className="container">
                    <div className="starter-template">
                        <div className="row">
                            <div className="col-md-12">
                                <div className="product-header">
                                    <h2><strong>Profile</strong></h2>
                                </div>
                            </div>
                            <div className="col-md-12">
                            <div className="form-horizontal" onSubmit={this.passwordReset}>
                                <div className="form-group">
                                    <label className="col-sm-3 control-label">Name</label>
                                    <label className="col-sm-8">{profile.name}</label>
                                </div>
                                <div className="form-group">
                                    <label className="col-sm-3 control-label">Email</label>
                                    <label className="col-sm-8">{profile.email}</label>
                                    {/*<label className="col-sm-8">{profile.email}</label>*/}
                                </div>
                            </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Account;