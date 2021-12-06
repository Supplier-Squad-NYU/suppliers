"""
Module: error_handlers
"""

from flask import jsonify
from service.supplier_exception import SupplierException
from . import app, status

@app.errorhandler(SupplierException)
def supplier_exception(error):
    """ Handles supplier exceptions as bad requests """
    return bad_request(error)


######################################################################
# Error Handlers
######################################################################
@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad requests with 400_BAD_REQUEST """
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_400_BAD_REQUEST, error=message),
        status.HTTP_400_BAD_REQUEST,
    )


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """Handles resources not found with 404_NOT_FOUND"""
    message = str(error)
    app.logger.warning(message)
    return (
        jsonify(status=status.HTTP_404_NOT_FOUND, error=message),
        status.HTTP_404_NOT_FOUND,
    )
