import React, {Component} from 'react';
import PropTypes from 'prop-types';
import ProductItem from '../productItem/ProductItem';
import { Grid } from 'semantic-ui-react';
import './Products.css';

class Products extends Component {
    render() {
        const productList = <Grid stackable columns='equal' centered>
        {this.props.productsData.map(product => <Grid.Column width={5} key={product.id}><ProductItem product={product} /></Grid.Column>)}
    </Grid>

        return (
            <ul className="product-list">
                {productList}
            </ul>
        );
    }
}

Products.propTypes = {
    productsData: PropTypes.array.isRequired
};

export default Products;