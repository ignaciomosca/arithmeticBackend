from pydantic import BaseModel, ConfigDict


class OperationModelDTO(BaseModel):
    """
    DTO for operation models.

    It returned when accessing operation models from the API.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class OperationModelInputDTO(BaseModel):
    """DTO for creating new operation model."""

    name: str
