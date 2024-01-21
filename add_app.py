import ast
import os
import sys


def add_app_to_installed_apps(app_name, project_path):
    settings_file_path = os.path.join(project_path, 'core', 'settings.py')

    try:
        with open(settings_file_path, 'r') as settings_file:
            settings_content = settings_file.read()

        # Parse the AST of the settings file
        tree = ast.parse(settings_content)

        # Check if the app is already in INSTALLED_APPS
        app_already_added = any(
            isinstance(node, ast.Str) and node.s == app_name
            for node in ast.walk(tree)
            if isinstance(node, ast.List) and node.elts
        )

        if app_already_added:
            return

        # Find the INSTALLED_APPS assignment node
        installed_apps_node = None
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Assign)
                and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == 'INSTALLED_APPS'
            ):
                installed_apps_node = node
                break

        if installed_apps_node is None:
            return

        # Add the app to INSTALLED_APPS
        installed_apps_node.value.elts.append(ast.Str(s=app_name))

        # Write the modified AST back to the settings file
        with open(settings_file_path, 'w') as settings_file:
            settings_file.write(ast.unparse(tree))
    except Exception as e:
        pass


if __name__ == "__main__":
    add_app_to_installed_apps(sys.argv[1], sys.argv[2])
