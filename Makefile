run-tests:

    @echo "Running funtional tests with django webtest"
    cd djangolabtests
    python manage.py test --where=functional_tests --jerbosity=2
