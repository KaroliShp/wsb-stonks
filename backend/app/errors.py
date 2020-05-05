from app import app


@app.errorhandler(404)
def not_found_error(error):
    return {'Message' : 'Not found'}, 404


@app.errorhandler(500)
def internal_error(error):
    app.logger.warning(error)
    return {'Message' : 'Internal errror'}, 500

@app.errorhandler(Exception)
def handle_unspecified_errors(error):
    app.logger.warning(error)
    return {'Message' : 'Undefined errror'}, 500