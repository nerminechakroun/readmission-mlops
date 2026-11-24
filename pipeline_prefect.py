from prefect import task, flow
from main import prepare, train, save, load, evaluate

import argparse

# ============================================================
# TASKS
# ============================================================


@task(name="install-dependencies")
def install_dependencies():
    import subprocess
    import sys

    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True
    )


@task(name="prepare-data")
def prepare_data_task():
    return prepare()


@task(name="train-model")
def train_model_task():
    return train()


@task(name="save-model")
def save_model_task():
    return save()


@task(name="load-model")
def load_model_task():
    return load()


@task(name="evaluate-model")
def evaluate_model_task():
    return evaluate()


@task(name="format-code")
def format_code_task():
    import subprocess

    files = ["model_pipeline.py", "main.py", "pipeline_prefect.py"]

    subprocess.run(["black"] + files, check=True)


@task(name="code-quality")
def code_quality_task():
    import subprocess

    files = ["model_pipeline.py", "main.py", "pipeline_prefect.py"]

    subprocess.run(["flake8"] + files, check=True)


@task(name="code-security")
def code_security_task():
    import subprocess

    files = ["model_pipeline.py", "main.py", "pipeline_prefect.py"]

    subprocess.run(["bandit", "-s", "B404,B603,B607"] + files, check=True)


@task(name="unit-tests")
def unit_tests_task():
    import subprocess

    subprocess.run(["pytest", "test_model_pipeline.py", "-v"], check=True)


# ============================================================
# FLOWS
# ============================================================


@flow(name="install")
def install_flow():
    install_dependencies()


@flow(name="clean")
def clean_flow():
    prepare_data_task()


@flow(name="train")
def train_flow():
    prepare_data_task()
    train_model_task()


@flow(name="code")
def code_flow():
    format_code_task()
    code_quality_task()
    code_security_task()
    unit_tests_task()


@flow(name="evaluate")
def evaluate_flow():
    load_model_task()
    evaluate_model_task()


@flow(name="all")
def all_flow():

    # Installation
    install_dependencies()

    # Tests et qualité du code
    code_flow()

    # Préparation des données
    prepare_data_task()

    # Entraînement
    train_model_task()

    # Sauvegarde
    save_model_task()

    # Évaluation
    evaluate_model_task()


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--flow", choices=["all", "install", "clean", "code", "evaluate"], required=True
    )

    args = parser.parse_args()

    if args.flow == "all":
        all_flow()

    elif args.flow == "install":
        install_flow()

    elif args.flow == "clean":
        clean_flow()

    elif args.flow == "code":
        code_flow()

    elif args.flow == "evaluate":
        evaluate_flow()
