from website import create_app # importing what I need from the created Python package

app = create_app()

if __name__ == '__main__': # only RUNNING this file, it runs the server (NOT importing)
    app.run()