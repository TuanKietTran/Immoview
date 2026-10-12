.PHONY: test lint typecheck build tf-check

test:
	cd django-core && SECRET_KEY=ci-test-secret DEBUG=true ALLOWED_HOSTS=localhost uv run pytest -q

lint:
	cd django-core && uv run ruff check apps/listings/domain/vietnam.py apps/listings/domain/entities.py apps/listings/tests config/test_settings.py

typecheck:
	cd django-core && SECRET_KEY=ci-test-secret DEBUG=true ALLOWED_HOSTS=localhost uv run mypy apps/listings/domain/vietnam.py apps/listings/domain/entities.py

build:
	cd cloud_front && pnpm build
	cd frontend-mis-islands && bun run build

tf-check:
	terraform -chdir=infra/terraform fmt -check -recursive
	terraform -chdir=infra/terraform/envs/staging init -backend=false
	terraform -chdir=infra/terraform/envs/staging validate
	terraform -chdir=infra/terraform/envs/dev init -backend=false
	terraform -chdir=infra/terraform/envs/dev validate
	terraform -chdir=infra/terraform/envs/prod init -backend=false
	terraform -chdir=infra/terraform/envs/prod validate
