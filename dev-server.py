from hypothesis import factory

if __name__ == '__main__':
    app = factory.create_app()
    app.run()
