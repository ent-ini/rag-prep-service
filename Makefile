run:
	uvicorn app.main:app --reload --port 8080

cli:
	python -m app.cli
