import os
import shutil
import subprocess


def get_maya_executable(version="2024"):
    if os.name == "nt":
        # Chemins d'installation par défaut pour Windows
        possible_paths = [
            f"C:/Program Files/Autodesk/Maya{version}/bin/maya.exe",
            f"C:/Program Files/Autodesk/Maya{version} Student/bin/maya.exe",
        ]
    elif os.name == "posix":
        if "darwin" in os.sys.platform:
            # Chemins d'installation par défaut pour macOS
            possible_paths = [
                f"/Applications/Autodesk/maya{version}/Maya.app/Contents/bin/maya",
                f"/Applications/Autodesk/maya{version} Student/Maya.app/Contents/bin/maya",
            ]
        else:
            # Chemins d'installation par défaut pour Linux
            possible_paths = [
                f"/usr/autodesk/maya{version}/bin/maya",
                f"/opt/autodesk/maya{version}/bin/maya",
            ]
    else:
        raise EnvironmentError("Unsupported platform: " + os.name)

    for path in possible_paths:
        if os.path.exists(path):
            return path

    raise FileNotFoundError(
        "Maya executable not found. Please specify the correct path."
    )


def get_maya_scripts_dir(version="2024"):
    # Détermine le répertoire des scripts utilisateur en fonction du système d'exploitation
    user_home = os.path.expanduser("~")
    if os.name == "nt":
        # Windows
        return os.path.join(user_home, "Documents", "maya", version, "scripts")
    elif os.name == "posix":
        # macOS ou Linux
        if "darwin" in os.sys.platform:
            # macOS
            return os.path.join(
                user_home,
                "Library",
                "Preferences",
                "Autodesk",
                "maya",
                version,
                "scripts",
            )
        else:
            # Linux
            return os.path.join(user_home, "maya", version, "scripts")
    else:
        raise EnvironmentError("Unsupported platform: " + os.name)


def install_plugin(plugin_src, maya_version="2024"):
    scripts_dir = get_maya_scripts_dir(maya_version)

    # Créer le répertoire des scripts s'il n'existe pas
    os.makedirs(scripts_dir, exist_ok=True)

    # Copier le plugin dans le répertoire des scripts
    plugin_dst = os.path.join(scripts_dir, os.path.basename(plugin_src))
    shutil.copy(plugin_src, plugin_dst)

    # Créer le script MEL pour configurer le raccourci
    mel_script = """
    if (`shelfLayout -ex "CustomTools"`) {
        shelfButton
            -parent "CustomTools"
            -label "SimpleWindow"
            -annotation "Open Simple PySide6 Window"
            -image1 "pythonFamily.png"
            -command "python(\\"import maya.cmds as cmds; cmds.showSimpleWindow()\\")";
    } else {
        shelfLayout -cellWidth 33 -cellHeight 33 "CustomTools";
        shelfButton
            -parent "CustomTools"
            -label "SimpleWindow"
            -annotation "Open Simple PySide6 Window"
            -image1 "pythonFamily.png"
            -command "python(\\"import maya.cmds as cmds; cmds.showSimpleWindow()\\")";
    }
    """

    mel_dst = os.path.join(scripts_dir, "setup_simple_window_shelf.mel")
    with open(mel_dst, "w") as file:
        file.write(mel_script)

    # Lancer Maya pour compléter l'installation
    maya_executable = get_maya_executable(
        "2024"
    )  # Changez en fonction de l'installation de Maya
    subprocess.run(
        [
            maya_executable,
            "-command",
            f'source "{mel_dst}"; loadPlugin "{plugin_dst}"',
        ]
    )


if __name__ == "__main__":
    plugin_src = "maya_main.py"  # Chemin vers votre fichier plugin
    install_plugin(plugin_src)
