from marshmallow import ValidationError, validates_schema


def validate_non_empty_string(data):
    if not data:
        raise ValidationError("string value should not be empty")

def validate_non_empty_list(data):
        if len(data) < 1:
            raise ValidationError("list must contain at least one item.")

def validate_non_empty_strings_in_list(data):
    for item in data:
        validate_non_empty_string(item)


# This schema is used when some input argument are optionnal
class WrongInputNameSchema:
    @validates_schema(pass_original=True)
    def wrong_input_name(self, data, orig_data):
        for ff in orig_data.keys():
            if ff not in self._declared_fields.keys():
                raise ValidationError("unknown argument passed.")


# This is used when all input arguments are required
class UnknownInputSchema:
    @validates_schema(pass_original=True)
    def no_extra_inputs(self, data, orig_data):
        if orig_data.keys() != self._declared_fields.keys():
            raise ValidationError("unknown argument passed.")


class ValidateNonEmptyFieldsSchema:
    @validates_schema
    def validate_non_empty_fields(self, data, **kwargs):
        for field_name, field_value in data.items():
            if not field_value:
                raise ValidationError(f"{field_name} should not be empty")