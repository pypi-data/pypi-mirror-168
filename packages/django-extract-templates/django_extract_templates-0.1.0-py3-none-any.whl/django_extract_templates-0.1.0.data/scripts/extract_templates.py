"""
    Copies Django's built-in templates and statics.
"""
import os
from pathlib import Path
from shutil import copytree
import sys
import logging
from typing import Optional, Tuple, List

logger = logging.getLogger("django_extract_templates")
logging.basicConfig(level=logging.DEBUG)

try:
    import django
except ImportError:
    logger.critical("Error: Django is not installed. Please install it.")
    sys.exit(1)


MODULES_WITH_TEMPLATES = ['admin', 'admindocs', 'auth', 'gis', 'postgres', 'sitemaps']
MODULES_WITH_JINJA2_TEMPLATES = ['postgres']
MODULES_WITH_STATICS = ['admin', 'gis']


def check_path(name: str, path: Path) -> None:
    if not path.exists():
        logger.critical("Error: Django %s dir not found, is your Django installation broken?\n"
                        "Path not found: %s", name, path)
        sys.exit(1)
    logger.info("Detected Django %s @ %s", name, path)


def copy_module_files(
    modules: List[str],
    contrib_path: Path,
    module_target: str,
    destination_path: Path
) -> None:
    for module in modules:
        module_path = contrib_path / module
        check_path(module, module_path)
        module_templates_path = module_path / module_target
        check_path(f'{module} {module_target}', module_templates_path)
        copytree(module_templates_path, destination_path, dirs_exist_ok=True)


def copy_static_files(
    contrib: Path,
    static_path: Path,
    exclude: List[str]
) -> None:
    modules_with_statics = include_modules(MODULES_WITH_STATICS, exclude)
    copy_module_files(modules_with_statics, contrib, 'static', static_path)


def copy_template_files(
    contrib: Path,
    templates_path: Path,
    jinja2_templates_path: Path,
    exclude: List[str]
) -> None:
    modules_with_templates = include_modules(MODULES_WITH_TEMPLATES, exclude)
    modules_with_jinja2_templates = include_modules(MODULES_WITH_JINJA2_TEMPLATES, exclude)
    copy_module_files(modules_with_templates, contrib, 'templates', templates_path)
    copy_module_files(modules_with_jinja2_templates, contrib, 'jinja2', jinja2_templates_path)


def ensure_path(name: str, path: Path) -> None:
    if not path.exists():
        logger.info("%s path does not exist, creating...", name)
        path.mkdir()
        logger.info("Created %s path @ %s", name, path)
        return
    logger.info("Detected %s path @ %s", name, path)


def get_django_contrib_path() -> Path:
    django_base_path = Path(sys.modules['django'].__path__[0]).resolve()
    logger.info(f"Detected Django @ {django_base_path}")
    contrib = django_base_path / 'contrib'
    check_path('contrib', contrib)
    return contrib


def include_modules(modules: List[str], excluded_modules: List[str]) -> List[str]:
    return [m for m in modules if m not in excluded_modules]


def run(
    copy_templates: bool = True,
    copy_statics: bool = True,
    static_root: Optional[str] = None,
    exclude: Optional[List[str]] = None
) -> None:
    contrib_path = get_django_contrib_path()
    templates_path, jinja2_templates_path, static_path = setup_base_paths(static_root)

    if not exclude:
        exclude = []

    if copy_templates:
        copy_template_files(contrib_path, templates_path, jinja2_templates_path, exclude)
    if copy_statics:
        copy_static_files(contrib_path, static_path, exclude)

    logger.info("Done!")


def setup_base_paths(static_root: Optional[str]) -> Tuple[Path, Path, Path]:
    base_path = Path(os.getcwd()).resolve()
    logger.info(f"BASE_DIR: {base_path}")
    templates_path = base_path / 'templates'
    ensure_path('templates', templates_path)
    jinja2_templates_path = base_path / 'jinja2'
    ensure_path('jinja2 templates', jinja2_templates_path)
    if not static_root:
        static_root = 'static'
    static_path = base_path / static_root
    ensure_path('static', static_path)
    return templates_path, jinja2_templates_path, static_path


if __name__ == '__main__':
    run()
