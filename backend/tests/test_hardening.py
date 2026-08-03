"""Regression tests for misc production-hardening fixes (audit P2-11, P2-22)."""

from __future__ import annotations

import asyncio
import shutil
import subprocess

import pytest
from agentflow import chat_service, git_service


def test_chat_send_rejects_unknown_provider(tmp_path):
    # An unknown provider must be rejected before any template lookup / launch (P2-11).
    res = asyncio.run(chat_service.send(tmp_path, "hi", provider="bogus"))
    assert res["status"] == "error"
    assert "bogus" in res["message"]


@pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")
def test_git_file_diff_refuses_env(tmp_path):
    # The untracked-file synthesis path must not surface .env contents (P2-22).
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True, capture_output=True)
    (tmp_path / ".env").write_text("SECRET=ghp_AAAAAAAAAAAAAAAAAAAAAAAA\n")
    res = asyncio.run(git_service.file_diff(tmp_path, ".env", staged=False))
    assert "ghp_" not in res["diff"]
    assert "not shown" in res["diff"]


@pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")
def test_git_file_diff_shows_normal_untracked_file(tmp_path):
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True, capture_output=True)
    (tmp_path / "notes.txt").write_text("hello world\n")
    res = asyncio.run(git_service.file_diff(tmp_path, "notes.txt", staged=False))
    assert "hello world" in res["diff"]


def test_ensure_workspace_backfills_missing_workspace_path(tmp_path):
    # A config.json written before workspacePath existed (or hand-edited) must be
    # healed, not returned as-is — set_workspace reads cfg["workspacePath"] and
    # would otherwise raise KeyError and 500 the workspace switch.
    from agentflow import config, paths

    config.ensure_workspace(tmp_path)
    cfg_file = paths.workspace_config_file(tmp_path)
    config.write_json(cfg_file, {"routing": {"engineer": "claude"}})  # no workspacePath

    cfg = config.ensure_workspace(tmp_path)

    assert cfg["workspacePath"] == str(tmp_path.resolve())
    assert config.read_json(cfg_file, {})["workspacePath"] == str(tmp_path.resolve())
    assert cfg["routing"] == {"engineer": "claude"}  # untouched
