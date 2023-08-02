from dotenv import dotenv_values, set_key


def change_mode():
    with open("fake_env_file.txt", "r") as fake_env_with_mode_test:
        new_info = fake_env_with_mode_test.read().replace(
            "MODE=TEST",
            "MODE=PROD",
        )

    with open("fake_env_file.txt", "w") as fake_env_with_mode_prod:
        fake_env_with_mode_prod.write(new_info)

    # changee .env
    env_values = dotenv_values('.env')
    env_values['MODE'] = 'PROD'
    set_key('.env', 'MODE', 'PROD')


if __name__ == '__main__':
    change_mode()
