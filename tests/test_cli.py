import sys

import pytest

from src.cli.main import cli


class TestCliDeploy:
    def test_deploy_missing_manifest_exits_nonzero(self, capsys, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["ao", "deploy", "missing-agent.yaml"])

        with pytest.raises(SystemExit) as exc_info:
            cli()

        captured = capsys.readouterr()
        assert exc_info.value.code == 2
        assert captured.out == ""
        assert "Manifest not found: missing-agent.yaml" in captured.err

    def test_deploy_existing_manifest_reports_progress(self, capsys, monkeypatch, tmp_path):
        manifest = tmp_path / "agent.yaml"
        manifest.write_text("name: test-agent\n")
        monkeypatch.setattr(sys, "argv", ["ao", "deploy", str(manifest)])

        cli()

        captured = capsys.readouterr()
        assert f"Deploying agent from manifest: {manifest}" in captured.out
        assert captured.err == ""
