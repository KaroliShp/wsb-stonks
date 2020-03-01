from app import app


@app.errorhandler(404)
def not_found_error(error):
    return {'Message' : 'Not found'}, 404


@app.errorhandler(500)
def internal_error(error):
    return {'Message' : 'Internal errror'}, 500