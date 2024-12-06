# Testing

## Unit Tests

### Run unit tests:

```bash
coverage run --source='.' --omit='manage.py,config/asgi.py,config/wsgi.py,todo_app/tests/test_e2e/*,todo_app/tests/test_integration/*' manage.py test todo_app.tests.test_unit
```

### Unit test coverage
```bash
coverage report -m
coverage html -d covhtml_unit
```
---

## Integration tests:

### Run integration tests:

```bash
coverage run --source='.' --omit='manage.py,config/asgi.py,config/wsgi.py,todo_app/tests/test_e2e/*,todo_app/tests/test_unit/*' manage.py test todo_app.tests.test_integration
```

### Integration test coverage
```bash
coverage report -m
coverage html -d covhtml_integration
```