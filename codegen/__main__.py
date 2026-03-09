from codegen.generate import models, resources, tests
from codegen.utils import load_config


def main() -> None:
    """Run code generation."""
    config = load_config()

    print("=== Generating models ===\n")
    models.run()

    print("\n=== Generating resources ===\n")
    resources.run()

    if config.get("with_tests", False):
        print("\n=== Generating tests ===\n")
        tests.run()

    print("\nAll done!")


if __name__ == "__main__":
    main()
