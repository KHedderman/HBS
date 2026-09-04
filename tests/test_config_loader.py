from agents.config_loader import env, load_config


def test_load_config_returns_dict_with_expected_top_level_keys():
    cfg = load_config()
    assert isinstance(cfg, dict)
    for key in ("system", "model_governance", "agents", "hitl_checkpoints", "logging"):
        assert key in cfg


def test_load_config_is_cached_singleton():
    # functools.lru_cache means both calls return the identical object,
    # not just equal content — this is what makes "one config, read
    # everywhere" actually true rather than aspirational.
    assert load_config() is load_config()


def test_load_config_director_list_is_nonempty_and_unique():
    cfg = load_config()
    directors = cfg["agents"]["directors"]
    ids = [d["id"] for d in directors]
    assert len(ids) >= 1
    assert len(ids) == len(set(ids))


def test_env_returns_default_when_unset(monkeypatch):
    monkeypatch.delenv("SOME_VAR_THAT_DOES_NOT_EXIST", raising=False)
    assert env("SOME_VAR_THAT_DOES_NOT_EXIST", "fallback") == "fallback"


def test_env_returns_actual_value_when_set(monkeypatch):
    monkeypatch.setenv("SOME_TEST_VAR", "real-value")
    assert env("SOME_TEST_VAR") == "real-value"
