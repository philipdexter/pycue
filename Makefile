

.PHONY: test
test:
	python -m pytest

.PHONY: golibcue
golibcue:
	cd golibcue/ && ./build.sh
