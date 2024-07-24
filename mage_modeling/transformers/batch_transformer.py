if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(batch, data, *args, **kwargs):
    # print(batch)
    # print(data)


    data["model"] = data["make"]+" " + data["model"]
    # Mapping dictionary
    column_mapping = {
        'mileage': 'mileage_in_km',
        'make': 'brand',
        'model': 'model',
        'fuel': 'fuel_type',
        'gear': 'transmission_type',
        'price': 'price_in_euro',
        'hp': 'power_ps',
        'year': 'year'
    }

    data.rename(columns=column_mapping, inplace=True)
    common_columns = data.columns.intersection(batch.columns)
    data = data[common_columns]
    
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
