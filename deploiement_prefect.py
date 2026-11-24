from prefect import serve

from pipeline_prefect import (
    all_flow,
    install_flow,
    clean_flow,
    code_flow,
    evaluate_flow,
    train_flow
)


if __name__ == "__main__":

    serve(
        all_flow.to_deployment(
            name="ml-pipeline-all",
            cron="15 12 * * *"
        ),

        install_flow.to_deployment(
            name="ml-pipeline-install",
            cron="0 9 * * *"
        ),

        clean_flow.to_deployment(
            name="ml-pipeline-clean",
            cron="30 9 * * *"
        ),

        code_flow.to_deployment(
            name="ml-pipeline-code",
            cron="0 11 * * *"
        ),

        evaluate_flow.to_deployment(
            name="ml-pipeline-evaluate",
            cron="0 13 * * *"
        ),

        train_flow.to_deployment(
            name="ml-pipeline-train",
            cron="0 10 * * *"
        )
    )

