from pydantic import BaseModel


class Request_additional_info(BaseModel):
    id: int
    rating: int
    comment: str

    def __str__(self):
        return f"ID: {self.id}, Rating: {self.rating}, Comment: {self.comment}"
