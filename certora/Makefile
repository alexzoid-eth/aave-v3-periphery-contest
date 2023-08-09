default: help

CONTRACTS_DIR = ../contracts/rewards

help:
	@echo "usage:"
	@echo "  make restore: reverts all unstaged changes in the src directory"
	@echo "  make bug: generates a patch containing a manually injected bug"
	@echo "  make bug_ma: generates a patch containing a manually injected bug (for multiAsset config)"

.SILENT: bug
bug:
	git diff certora -- $(CONTRACTS_DIR) > tests/participants/bug$$(find tests/participants -type f -name "bug*.patch" | sort -t 'g' -k 2n | tail -n 1 | tr -dc '0-9' | awk '{$$1=$$1+1; print}').patch

.SILENT: bug_ma
bug_ma:
	git diff certora -- $(CONTRACTS_DIR) > tests/participants/bug$$(find tests/participants -type f -name "bug*.patch" | sort -t 'g' -k 2n | tail -n 1 | tr -dc '0-9' | awk '{$$1=$$1+1; print}')_multiAsset.patch

restore:
	git restore $(CONTRACTS_DIR)/*
