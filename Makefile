test: ## run tests
	cd api; pipenv run py.test -rx --cov-config=.coveragerc --cov=.

run-api-old:
	cd api; pipenv run python -m app

run-api:
	cd api; serverless offline --reloadHandler

deploy-frontend:
	cd app; serverless client deploy --no-confirm

deploy-backend:
	cd api; serverless deploy --stage $(STAGE)