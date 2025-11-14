from os import getenv
from shutil import copytree, copy2
from sys import exit
from pathlib import Path

REQUIRED_ITEMS = [
    Path("Cursor/settings.json"),
    Path("Cursor/keybindings.json"),
]


def locate_required_items(project_root: Path) -> dict[str, Path]:
    # make sure files exist
    found: dict[str, Path] = {}
    missing: list[Path] = []

    for relative_path in REQUIRED_ITEMS:
        candidate = project_root / relative_path
        if candidate.exists():
            found[relative_path.name] = candidate
        else:
            missing.append(relative_path)

    if missing:
        missing_list = ", ".join(str(item) for item in missing)
        print(f"Required items not found: {missing_list}")
        exit(1)

    return found


def resolve_target_directory() -> Path:
    # try the default Cursor roaming path first
    appdata = getenv("APPDATA")
    if appdata:
        default_target = Path(appdata) / "Cursor" / "User"
        if default_target.is_dir():
            return default_target

        # if Cursor isn't under the usual roaming location, fall back to manual input
        print(f"Default Cursor path not found: {default_target}")
    else:
        # in case APPDATA is missing ask for install path
        print("APPDATA environment variable is not set.")

    # trim quotes so copy-pasted Explorer paths work
    user_input = input("Enter the full path to your Cursor directory: ").strip().strip('"')
    if not user_input:
        print("No path provided. Unable to continue.")
        exit(1)

    candidate = Path(user_input).expanduser()

    if candidate.is_dir():
        if candidate.name.lower() == "user":
            return candidate
        user_subdir = candidate / "User"
        if user_subdir.is_dir():
            return user_subdir

    # if cannot find dirs terminate script 
    print("Unable to locate a valid Cursor 'User' directory with the provided path.")
    exit(1)


def copy_required_items(items: dict[str, Path], target_dir: Path) -> None:
    # copy each file or folder over, keeping the backup intact
    try:
        for name, source in items.items():
            destination = target_dir / name

            if source.is_dir():
                # move entire folder
                copytree(source, destination, dirs_exist_ok=True)
            else:
                # ensure the parent directory exists, then copy file
                destination.parent.mkdir(parents=True, exist_ok=True)
                copy2(source, destination)

            print(f"Copied {source} -> {destination}")
    except Exception as E:
        print(f"Failed to copy files: {E}")
        exit(1)


def main() -> None:
    # resolve paths, copy files, and report success
    project_root: Path = Path(__file__).resolve().parent
    items: dict[str, Path] = locate_required_items(project_root)
    target_dir: Path = resolve_target_directory()
    copy_required_items(items, target_dir)
    print("Cursor settings restored successfully.")


if __name__ == "__main__":
    main()

