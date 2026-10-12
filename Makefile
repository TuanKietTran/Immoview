.PHONY: test lint typecheck build tf-check

test:
	cd django-core && uv run pytest -q

lint:
	cd django-core && uv run ruff check .

typecheck:
	cd django-core && uv run mypy apps config

build:
	cd cloud_front && pnpm build
	cd frontend-mis-islands && bun run build

tf-check:
	terraform -chdir=infra/terraform fmt -check -recursive
	terraform -chdir=infra/terraform/envs/staging init -backend=false
	terraform -chdir=infra/terraform/envs/staging validate
	terraform -chdir=infra/terraform/envs/prod init -backend=false
	terraform -chdir=infra/terraform/envs/prod validate
