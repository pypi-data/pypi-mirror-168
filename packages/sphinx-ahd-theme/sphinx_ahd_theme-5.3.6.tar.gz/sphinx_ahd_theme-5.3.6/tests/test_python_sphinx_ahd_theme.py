import sphinx_ahd_theme


def test_theme_info():
    assert isinstance(sphinx_ahd_theme.__version__, str)
    assert len(sphinx_ahd_theme.__version__) >= 5


def test_module_methods():
    assert isinstance(sphinx_ahd_theme.get_html_theme_path(), str)
