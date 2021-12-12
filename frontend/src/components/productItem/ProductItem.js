import React, {Component} from 'react';
import PropTypes from 'prop-types';
import './ProductItem.css';
import { Card } from 'semantic-ui-react';

class ProductItem extends Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.productDescription = this.productDescription.bind(this);
        this.productHeaderClasses = this.productHeaderClasses.bind(this);
        this.state = {hidden: true};
    }

    productHeaderClasses() {
        return this.state.hidden ?
            'product__header' : 'product__header product__header--bold';
    }

    productDescription() {
        if (!this.state.hidden) {
            return (
                <div className="product__description">
                    {this.props.description}
                </div>
            );
        }
        return null;
    }

    handleClick() {
        this.setState({
            hidden: !this.state.hidden
        });
    }

    render() {
        return (
            <Card 
                //image={this.props.image}
                header={this.props.name}
                meta={this.props.price}
                description={this.props.description}
            />
        );
    }
}

ProductItem.propTypes = {
    //image: PropTypes.string,
    name: PropTypes.string.isRequired,
    code: PropTypes.number,
    price: PropTypes.number,
    description: PropTypes.string
};

export default ProductItem;