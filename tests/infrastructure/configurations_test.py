import dotenv
from dotenv.main import DotEnv


def test_that_local_dotenv_file_and_dotenv_template_have_the_same_structure():
    env_template_dict = DotEnv(dotenv.find_dotenv(".env.template"))
    comparable = DotEnv(dotenv.find_dotenv()).dict()

    actual_keys = set(comparable.keys())
    expected_keys = set(env_template_dict.dict().keys())

    missing = expected_keys - actual_keys

    assert (
        not missing
    ), f"Missing keys from the environment or .env file: \n{missing}"


# TODO: create a test that checks the files for the expression "only for development"
