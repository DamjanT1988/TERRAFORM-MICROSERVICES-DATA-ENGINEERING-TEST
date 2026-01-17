compose-up:
	docker compose up --build

compose-down:
	docker compose down -v

lint:
	ruff check services tests

format:
	black services tests

test:
	pytest -q

terraform-fmt:
	cd infra/terraform && terraform fmt -recursive
