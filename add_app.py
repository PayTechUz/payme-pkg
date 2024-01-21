import os
import sys


def add_app_to_installed_apps(app_name, project_path):
    settings_file_path = os.path.join(project_path, 'core', 'settings.py')

    try:
        with open(settings_file_path, 'r') as settings_file:
            settings_content = settings_file.read()

        # Check if the app is already in INSTALLED_APPS
        if f"'{app_name}'," in settings_content:
            return

        # Add the app to INSTALLED_APPS
        with open(settings_file_path, 'a') as settings_file:
            settings_file.write(f"\n    '{app_name}',  # Added by GitHub Actions\n")
    except Exception:
        pass


if __name__ == "__main__":
    add_app_to_installed_apps(sys.argv[1], sys.argv[2])
