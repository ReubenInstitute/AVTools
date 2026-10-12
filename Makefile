PYPI_TOKEN ?= ~/pypi.txt

.PHONY: pip install-pip deb install-deb upload clean

pip:
	rm -rf build
	mkdir -p build
	cp Media.py Services.py pip/pyproject.toml GPL-3 build/
	( cd build && python3 -m build --outdir . )

install-pip:
	python3 -m pip install build/*.whl

deb:
	rm -rf build/deb
	mkdir -p build/deb
	cp -r debian build/deb/
	cp Media.py Services.py GPL-3 README.md build/deb/
	( cd build/deb && dpkg-buildpackage -us -uc -b )

install-deb:
	dpkg -i build/python3-avtools_*.deb

upload:
	TWINE_USERNAME=__token__ TWINE_PASSWORD=$$(cat $(PYPI_TOKEN)) twine upload build/*.whl build/*.tar.gz

clean:
	rm -rf build
