import factory


def mem_user_generator():
    seq = 0

    def user_generator(ignored):
        nonlocal seq
        seq += 1
        return f'testuser{seq}'
    return user_generator


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'users.User'
        django_get_or_create = ('username',)

    id = factory.Faker('uuid4')
    username = factory.Sequence(mem_user_generator())
    password = factory.Faker('password', length=10, special_chars=True, digits=True,
                             upper_case=True, lower_case=True)
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True
    is_staff = False
