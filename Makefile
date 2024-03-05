SHELL := bash

.PHONY: tar clean pre-test post-test patch automator

automator:
ifndef TERGET
	$(error macro TERGET must be provided)
else
	@cd ..; \
	echo "Generating field.json: $(TERGET)..."; \
	python -m filler.tools.gen_field_json "$(TERGET)"; \
	echo "Generating test data: $(TERGET)..."; \
	python -m filler.tools.gen_test_data "$(TERGET)"
endif
pre-test:
	@cd ..; \
	echo "Try to fill pdf with pre-convert data..."; \
	python -m filler.test.pre_convert "$(TERGET)"
post-test:
	@cd ..; \
	echo "Try to fill pdf with post-convert data..."; \
	python -m filler.test.post_convert "$(TERGET)"
tar:
	git archive HEAD -o filler.zip
clean:
	rm filler.zip
patch:
	src=$(python3 -c "import site;print(site.getsitepackages()[0])"); \
	src=$src/fitz/fitz.py; \
	patch $src < tools/fitz.patch; \
