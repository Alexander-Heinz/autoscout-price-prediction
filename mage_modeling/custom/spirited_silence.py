if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from sklearn.metrics import mean_squared_error


@custom
def transform_custom(data, *args, **kwargs):

    preds = data[0]
    y_val = data[1]

    #print(y_val)
    print(mean_squared_error(y_val, preds, squared=False))

    # Specify your custom logic here

    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
