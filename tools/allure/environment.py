from config import settings
import sys, platform

def create_allure_environment_file():
    items = [f'{key}={value}'for key, value in settings.model_dump().items()]
    items.append("os_info="f'{platform.system()}, {platform.release()}',)
    items.append("python_version="f'{sys.version}')

    properties = '\n'.join(items)

    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w+') as file:
        file.write(properties)