if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import numpy as np
from sklearn.metrics import mean_squared_error

@transformer
def transform(final_model_pipeline, data, *args, **kwargs):

    X_val = data.drop('price_in_euro', axis=1)
    y_val = data['price_in_euro']
    
    preds = final_model_pipeline.predict(X_val)
    print(mean_squared_error(y_val, preds, squared=False))

    return preds


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
