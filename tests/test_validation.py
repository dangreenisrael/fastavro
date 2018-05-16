from fastavro.validate import validate, ValidationError
import pytest

schema = {
    "fields": [
        {
            "name": "str_null",
            "type": ["null", "string"]
        },
        {
            "name": "str",
            "type": "string"
        },
        {
            "name": "integ_null",
            "type": ["null", "int"]
        },
        {
            "name": "integ",
            "type": "int"
        }
    ],
    "namespace": "namespace",
    "name": "missingerror",
    "type": "record"
}


def validation_boolean(schema, *records):
    return all(
        validate(record, schema, raise_errors=False)
        for record in records
    )


def validation_raise(schema, *records):
    return all(
        validate(record, schema, raise_errors=True)
        for record in records
    )


def test_validate_string_in_int_raises():
    records = [{
        'str_null': 'str',
        'str': 'str',
        'integ_null': 'str',
        'integ': 21,
    }]

    with pytest.raises((ValidationError,)):
        validation_raise(schema, *records)


def test_validate_string_in_int_false():
    records = [{
        'str_null': 'str',
        'str': 'str',
        'integ_null': 'str',
        'integ': 21,
    }]

    assert validation_boolean(schema, *records) is False


def test_validate_true():
    records = [
        {'str_null': 'str', 'str': 'str', 'integ_null': 21, 'integ': 21, },
        {'str_null': None, 'str': 'str', 'integ_null': None, 'integ': 21, },
    ]

    assert validation_boolean(schema, *records) is True


def test_validate_string_in_int_null_raises():
    records = [{
        'str_null': 'str',
        'str': 'str',
        'integ_null': 11,
        'integ': 'str',
    }]
    with pytest.raises((ValidationError,)):
        validation_raise(schema, *records)


def test_validate_string_in_int_null_false():
    records = [{
        'str_null': 'str',
        'str': 'str',
        'integ_null': 11,
        'integ': 'str',
    }]

    assert validation_boolean(schema, *records) is False


def test_validate_int_in_string_null_raises():
    records = [{
        'str_null': 11,
        'str': 'str',
        'integ_null': 21,
        'integ': 21,
    }]
    with pytest.raises((ValidationError,)):
        validation_raise(schema, *records)


def test_validate_int_in_string_null_false():
    records = [{
        'str_null': 11,
        'str': 'str',
        'integ_null': 21,
        'integ': 21,
    }]
    assert validation_boolean(schema, *records) is False


def test_validate_int_in_string_raises():
    records = [{
        'str_null': 'str',
        'str': 11,
        'integ_null': 21,
        'integ': 21,
    }]

    with pytest.raises((ValidationError,)):
        validation_raise(schema, *records)


def test_validate_int_in_string_false():
    records = [{
        'str_null': 'str',
        'str': 11,
        'integ_null': 21,
        'integ': 21,
    }]

    assert validation_boolean(schema, *records) is False


def test_validate_null_in_string_raises():
    records = [{
        'str_null': 'str',
        'str': None,
        'integ_null': 21,
        'integ': 21,
    }]

    with pytest.raises((ValidationError,)):
        validation_raise(schema, *records)


def test_validate_null_in_string_false():
    records = [{
        'str_null': 'str',
        'str': None,
        'integ_null': 21,
        'integ': 21,
    }]

    assert validation_boolean(schema, *records) is False
