import subprocess
from pathlib import Path


def test_gen_cdk_conf():
    cwd = Path(__file__).parents[1].joinpath("demo_app")
    completed_process = subprocess.run(["gen-cdk-conf", "src", "cdk_conf.json"], cwd=cwd)
    assert completed_process.returncode == 0


def test_open_api_spec():
    cwd = Path(__file__).parents[1].joinpath("demo_app")
    completed_process = subprocess.run(["gen-open-api-spec", "src", "open_api_spec.json"], cwd=cwd)
    assert completed_process.returncode == 0
