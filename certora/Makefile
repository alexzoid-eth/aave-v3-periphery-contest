default: help

CONTRACTS_DIR = ../contracts/rewards

help:
	@echo "usage:"
	@echo "  make restore: reverts all unstaged changes in the src directory"
	@echo "  make bug: generates a patch containing a manually injected bug"

.SILENT: bug
bug:
	git diff certora -- $(CONTRACTS_DIR) > tests/participants/bug$$(find tests/participants -type f -name "bug*.patch" | sort -t 'g' -k 2n | tail -n 1 | tr -dc '0-9' | awk '{$$1=$$1+1; print}').patch

restore:
	git restore $(CONTRACTS_DIR)/*
