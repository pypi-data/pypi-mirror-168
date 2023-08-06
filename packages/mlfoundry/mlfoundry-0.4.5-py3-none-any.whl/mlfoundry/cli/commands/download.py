import click

from mlfoundry import ModelVersion, get_client


@click.group(help="Download model logged with Mlfoundry")
def download():
    ...


@download.command(short_help="Download a logged model")
@click.option(
    "--fqn",
    required=True,
    type=str,
    help="fqn of the model version",
)
@click.option(
    "--path",
    type=click.Path(file_okay=False, dir_okay=True, exists=False),
    required=True,
    help="path where the model will be downloaded",
)
def model(fqn: str, path: str):
    """
    Download the logged model for a run.\n
    """
    get_client()  # TODO (chiragjn): should give an option for custom tracking uri
    model_version = ModelVersion(fqn=fqn)
    download_path = model_version.download(path=path)
    print(f"Downloaded model files to {download_path}")
