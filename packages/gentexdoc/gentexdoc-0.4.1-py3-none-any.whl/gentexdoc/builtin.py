from typing import Dict


# Constants

BUILTIN_OBJECT = "builtin"


# Utility functions

def create_builtin_context(context: Dict):
    context[BUILTIN_OBJECT] = {
        "packages": get_required_packages()
    }


def get_required_packages() -> str:
    packages = "\\usepackage{lmodern}\n"
    packages += "\\usepackage{hyperref}\n"
    packages += "\\usepackage{longtable}\n"
    packages += "\\usepackage{booktabs}\n"

    return packages
