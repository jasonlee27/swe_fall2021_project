import React, {Component} from 'react'
import Modal from "react-bootstrap/lib/Modal";
import {errorMsg, successMsg} from '../../components/notification/ToastNotification';
import Products from '../../components/products/Products';
import Pagination from 'react-bootstrap/lib/Pagination';
import api from '../../api';
import Barcode from '../../components/scan/barcode';
import Webcam from '../../components/scan/react-webcam';
import Cart from '../../components/cart';

class ProductPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            product: {
                id: 0,
                name:'',
                image: '',
                code:'',
                price:''
            },
            cart: [],
            products: [{
                id: 0,
                name:'Apples',
                image: '../../assets/images/apples.webp',
                code:'0000',
                price:'$210'
            },{
                id: 1,
                name:'Oranges',
                image: '../../assets/images/oranges.webp',
                code:'0001',
                price:'$100'
            }],
            updateDlgFlg: false,
            deleteDlgFlg: false,
            current: 0,
            limit: 5,
            totalElements : 0,
            totalPages : 0
        };
        this.loadProducts();
    }

    componentDidUpdate(prevProps, prevState) {
        if (prevState.current !== this.state.current) {
            this.loadProducts();
        }
    }


    loadProducts = () => {
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

        self.setState({ products: [{
            id: 0,
            name:'Apples',
            code:'0000',
            price:'$210'
        },{
            id: 1,
            name:'Oranges',
            code:'0001',
            price:'$100'
        }]});
        self.setState({current: 2});
        self.setState({totalPages: 1});
        self.setState({totalElements: 2});
    };

    addProduct = (product) => {
        this.setState({cart: [...this.state.cart, product]})
    };
    
    getToCheckout = () => {};

    deleteProduct = (product) => {
        var array = [...this.state.cart]; // make a separate copy of the array
        console.log("array: ", array)
        console.log("product: ", product)
        var index = array.indexOf(product)
        console.log("index:",index)
        if (index !== -1) {
          array.splice(index, 1);
          this.setState({cart: array});
        }
        this.setState({deleteDlgFlg:false})
    };

    // ---------Update Dialog open/close--------
    handleUpdateDlgClose() {
        this.setState({updateDlgFlg: false});
    };

    handleUpdateDlgShow(data) {
        this.setProductToState(data);
        this.setState({updateDlgFlg: true});
    };

    // ---------Delete Dialog open/close--------
    handleDeleteDlgClose() {
        this.setState({deleteDlgFlg: false});
    };

    handleDeleteDlgShow(data) {
        this.setProductToState(data);
        this.setState({deleteDlgFlg: true});
    };

    setProductToState(data) {
        const {product} = this.state;
        if (data !== null) {
            product.id = data.id;
            product.name = data.name;
            product.code = data.code;
            product.price = data.price;
            this.setState({product});
        }
    };

    onPaginationChange(current){
        console.log(current);
        this.setState({
            current: current,
        });

    };

    paginationPrev() {
        const {current} = this.state;
        if (current !== 0)
            this.setState({
                current: current - 1,
            });
    }

    paginationNext(){
        const {current, totalPages} = this.state;
        if(current < totalPages)
            this.setState({
                current: current + 1,
            });
    }

    render() {
        const {products, product, updateDlgFlg, deleteDlgFlg, current, totalPages, cart} = this.state;
        let productItem = [];
        let cartTotal = Object.keys(cart).length
        let totalElements = Object.keys(products).length
        for (let number = 0; number <= totalPages; number++) {
            productItem.push(
                <Pagination.Item active={number === current} onClick={() => this.onPaginationChange(number)}>{number+1}</Pagination.Item>
            );
        }
        
        let cartComponent =  <div className="product">
                <button className='btn btn-primary' onClick={this.getToCheckout}> Cart ({cartTotal})</button>
            </div>

        let productsComponent = products.map((product) =>
            <div className="product">
                <h4><strong>{product.id}</strong></h4>
                <img src={product.image} alt={product.image}></img>
                <p>{product.body}</p>
                <strong>{product.name}</strong>
                <br/> <br/>
                <button className='btn btn-primary' onClick={() => this.addProduct(product)}> Add</button>
                &nbsp; &nbsp; &nbsp;
                <button className='btn btn-primary' onClick={() => this.deleteProduct(product)}> Delete</button>
                <hr/>
            </div>
        );

        return (
            <div>
                <div className="container">
                    <div className="starter-template">
                        <div className="row">
                            <div className="col-md-12">
                                <div className="product-header">
                                    <h2><strong>Reader</strong></h2>
                                    <Barcode/>
                                    <Webcam />
                                </div>
                            </div>
                            <div className="col-md-12">
                                <div className="product-header">
                                    <h2><strong>Cart</strong></h2>
                                    {cartComponent}
                                </div>
                            </div>
                            <div className="col-md-12">
                                <div className="product-header">
                                    <h2><strong>Products</strong></h2>
                                    {console.log("products: ",this.state.products)}
                                    {productsComponent}
                                    {/*<Products productsData={this.state.products}/>*/}
                                </div>
                            </div>
                            <div className="col-md-12">
                                <div className="pagination-div">
                                    <span>Total Products: {totalElements}</span><br/>
                                    <Pagination bsSize="medium">
                                        <Pagination.Prev onClick={() => this.paginationPrev()}/>
                                        {productItem}
                                        <Pagination.Next onClick={() => this.paginationNext()} />
                                    </Pagination>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                

                <Modal
                    show={updateDlgFlg}
                    onHide={() => this.handleUpdateDlgClose()}
                    aria-labelledby="ModalHeader"
                >
                    <form onSubmit={this.addProduct}>
                        <Modal.Header closeButton>
                            <Modal.Title id='ModalHeader'>Product Update</Modal.Title>
                        </Modal.Header>

                        <Modal.Body>
                            <div className="form-horizontal">
                                <div className="form-group">
                                    <label className="col-sm-2 control-label">Title* </label>

                                    <div className="col-sm-10">
                                        <input type="text" className="form-control" id="title" name="title"
                                               placeholder="Title"
                                               value={product.id}
                                               maxLength="512"
                                               onChange={(e) => this.setState({
                                                   product: {
                                                       ...product,
                                                       title: e.target.value
                                                   }
                                               })}
                                               required="true"/>
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label className="col-sm-2 control-label">Body* </label>
                                    <div className="col-sm-10">
                                         <textarea rows="20" className="form-control" id="body" name="body"
                                                   maxLength="65535"
                                                   value={product.body}
                                                   onChange={(e) => this.setState({product: {...product, body: e.target.value}})}
                                                   placeholder="Full Product . . ." required="true">
                                         </textarea>
                                    </div>
                                </div>

                                <div className="form-group">
                                    <label className="col-sm-2 control-label">Author Name*</label>

                                    <div className="col-sm-10">
                                        <input type="text" className="form-control" id="author" name="author"
                                               value={product.name}
                                               maxLength="225"
                                               onChange={(e) => this.setState({
                                                   product: {
                                                       ...product,
                                                       author: e.target.value
                                                   }
                                               })}
                                               placeholder="Author Name"
                                               required="true"/>
                                    </div>
                                </div>
                            </div>
                        </Modal.Body>
                        <Modal.Footer>
                            <button className='btn btn-primary' type="button" onClick={() => this.handleUpdateDlgClose()}>
                                Cancel
                            </button>
                            <button className='btn btn-primary' type="submit">
                                Update
                            </button>
                        </Modal.Footer>
                    </form>
                </Modal>

                <Modal
                    show={deleteDlgFlg}
                    onHide={() => this.handleDeleteDlgClose()}
                    aria-labelledby="ModalHeader"
                >
                    <Modal.Header closeButton>
                        <Modal.Title id='ModalHeader'>Delete Product</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <p>Do want to Delete Product ?</p>
                    </Modal.Body>
                    <Modal.Footer>
                        <button className='btn btn-primary' type="button" onClick={() => this.handleDeleteDlgClose()}>
                            No
                        </button>
                        &nbsp; &nbsp;
                        <button className='btn btn-primary' onClick={this.deleteProduct}>
                            Yes
                        </button>
                    </Modal.Footer>
                </Modal>
            </div>
        )
    }
}

export default ProductPage;