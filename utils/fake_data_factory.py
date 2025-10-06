import random
from faker import Faker


class FakeDataFactory:
    def __init__(self, faker: Faker):
        self.__faker = faker

    def integer(self, start: int = 1, end: int = 30, step: int = 1) -> int:
        return self.__faker.random_int(min=start, max=end, step=step)

    def email(self, domain: str | None = None) -> str:
        return self.__faker.email(domain=domain)
    
    def password(self) -> str:
        return self.__faker.password()
    
    def first_name(self) -> str:
        return self.__faker.first_name()
    
    def last_name(self) -> str:
        return self.__faker.last_name()
    
    def middle_name(self) -> str:
        return self.__faker.first_name()
    
    def estimated_time(self) -> str:
        return f"{self.integer(start=2, end=10)} weeks"
    
    def description(self) -> str:
        return self.__faker.sentence(nb_words=15)
    
    def title(self, word_count: int = 4) -> str:
        return self.__faker.sentence(nb_words=word_count)
    
    def min_score(self) -> int:
        return self.integer(start=10, end=30)
    
    def max_score(self) -> int:
        return self.integer(start=50, end=100)
    
    def uuid4(self) -> str:
        return self.__faker.uuid4()
    
    def file_path(self) -> str:
        return self.__faker.file_path(depth=4, extension=".jpeg")


faker = FakeDataFactory(faker=Faker())