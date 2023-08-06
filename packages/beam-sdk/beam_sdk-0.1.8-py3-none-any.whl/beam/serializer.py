from beam.exceptions import BeamSerializationError
from beam.types import Types
from marshmallow import Schema, fields, validate


class BaseSerializer(Schema):
    def validate_and_dump(self, data):
        validation_errors = self.validate(data)

        if len(validation_errors) > 0:
            raise BeamSerializationError(
                f"{self.__class__.__name__}\n{validation_errors}"
            )
        return self.dump(dict)

    def validate(self, data, raise_exception=False, **kwargs):
        if raise_exception:
            validation_errors = self.validate(data)

            if len(validation_errors) > 0:
                raise BeamSerializationError(
                    f"{self.__class__.__name__}\n{validation_errors}"
                )
        return super().validate(data, **kwargs)

    class Meta:
        ordered = True


class AppConfigurationSerializer(BaseSerializer):
    name = fields.String(required=True, validate=validate.Length(max=128))
    cpu = fields.Integer(required=True)
    gpu = fields.Integer(required=True)
    memory = fields.String(required=True)
    apt_install = fields.List(fields.String(), required=True)
    python_runtime = fields.String(required=True)
    python_packages = fields.List(fields.String(), required=True)
    workspace = fields.String(required=True)


class BaseTriggerSerializer(BaseSerializer):
    inputs = fields.Dict(
        keys=fields.String(),
        values=fields.String(validate=validate.OneOf(Types.to_list())),
    )

    outputs = fields.Dict(
        keys=fields.String(),
        values=fields.String(validate=validate.OneOf(Types.to_list())),
    )


class CronJobTriggerSerializer(BaseTriggerSerializer):
    # TODO: Validation step needs to be handled somewhere
    cron_schedule = fields.String()
