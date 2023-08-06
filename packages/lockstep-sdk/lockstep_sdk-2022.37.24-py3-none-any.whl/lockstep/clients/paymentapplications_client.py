#
# Lockstep Platform SDK for Python
#
# (c) 2021-2022 Lockstep, Inc.
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
# @author     Lockstep Network <support@lockstep.io>
# @copyright  2021-2022 Lockstep, Inc.
# @link       https://github.com/Lockstep-Network/lockstep-sdk-python
#

from lockstep.lockstep_response import LockstepResponse
from lockstep.models.errorresult import ErrorResult
from lockstep.fetch_result import FetchResult
from lockstep.models.actionresultmodel import ActionResultModel
from lockstep.models.paymentappliedmodel import PaymentAppliedModel

class PaymentApplicationsClient:
    """
    API methods related to PaymentApplications
    """
    from lockstep.lockstep_api import LockstepApi

    def __init__(self, client: LockstepApi):
        self.client = client

    def retrieve_payment_application(self, id: str, include: str) -> LockstepResponse[PaymentAppliedModel]:
        """
        Retrieves the Payment Application specified by this unique
        identifier, optionally including nested data sets.

        A Payment Application is created by a business who receives a
        Payment from a customer. A customer may make a single Payment to
        match an Invoice exactly, a partial Payment for an Invoice, or a
        single Payment may be made for multiple smaller Invoices. The
        Payment Application contains information about which Invoices
        are connected to which Payments and for which amounts.

        Parameters
        ----------
        id : str
            The unique Lockstep Platform ID number of this Payment
            Application; NOT the customer's ERP key
        include : str
            To fetch additional data on this object, specify the list of
            elements to retrieve. Available collections: Invoice,
            Payment
        """
        path = f"/api/v1/PaymentApplications/{id}"
        result = self.client.send_request("GET", path, None, {"include": include}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, PaymentAppliedModel(**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def update_payment_application(self, id: str, body: object) -> LockstepResponse[PaymentAppliedModel]:
        """
        Updates an existing Payment Application with the information
        supplied to this PATCH call.

        The PATCH method allows you to change specific values on the
        object while leaving other values alone. As input you should
        supply a list of field names and new values. If you do not
        provide the name of a field, that field will remain unchanged.
        This allows you to ensure that you are only updating the
        specific fields desired.

        A Payment Application is created by a business who receives a
        Payment from a customer. A customer may make a single Payment to
        match an Invoice exactly, a partial Payment for an Invoice, or a
        single Payment may be made for multiple smaller Invoices. The
        Payment Application contains information about which Invoices
        are connected to which Payments and for which amounts.

        Parameters
        ----------
        id : str
            The unique Lockstep Platform ID number of the Payment
            Application to update; NOT the customer's ERP key
        body : object
            A list of changes to apply to this Payment Application
        """
        path = f"/api/v1/PaymentApplications/{id}"
        result = self.client.send_request("PATCH", path, body, {}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, PaymentAppliedModel(**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def delete_payment_application(self, id: str) -> LockstepResponse[ActionResultModel]:
        """
        Deletes the Payment Application referred to by this unique
        identifier.

        A Payment Application is created by a business who receives a
        Payment from a customer. A customer may make a single Payment to
        match an Invoice exactly, a partial Payment for an Invoice, or a
        single Payment may be made for multiple smaller Invoices. The
        Payment Application contains information about which Invoices
        are connected to which Payments and for which amounts.

        Parameters
        ----------
        id : str
            The unique Lockstep Platform ID number of the Payment
            Application to delete; NOT the customer's ERP key
        """
        path = f"/api/v1/PaymentApplications/{id}"
        result = self.client.send_request("DELETE", path, None, {}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, ActionResultModel(**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def create_payment_applications(self, body: list[PaymentAppliedModel]) -> LockstepResponse[list[PaymentAppliedModel]]:
        """
        Creates one or more Payment Applications within this account and
        returns the records as created.

        A Payment Application is created by a business who receives a
        Payment from a customer. A customer may make a single Payment to
        match an Invoice exactly, a partial Payment for an Invoice, or a
        single Payment may be made for multiple smaller Invoices. The
        Payment Application contains information about which Invoices
        are connected to which Payments and for which amounts.

        Parameters
        ----------
        body : list[PaymentAppliedModel]
            The Payment Applications to create
        """
        path = "/api/v1/PaymentApplications"
        result = self.client.send_request("POST", path, body, {}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, list[PaymentAppliedModel](**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def query_payment_applications(self, filter: str, include: str, order: str, pageSize: int, pageNumber: int) -> LockstepResponse[FetchResult[PaymentAppliedModel]]:
        """
        Queries Payment Applications for this account using the
        specified filtering, sorting, nested fetch, and pagination rules
        requested.

        More information on querying can be found on the [Searchlight
        Query Language](https://developer.lockstep.io/docs/querying-with-searchlight)
        page on the Lockstep Developer website.

        A Payment Application is created by a business who receives a
        Payment from a customer. A customer may make a single Payment to
        match an Invoice exactly, a partial Payment for an Invoice, or a
        single Payment may be made for multiple smaller Invoices. The
        Payment Application contains information about which Invoices
        are connected to which Payments and for which amounts.

        Parameters
        ----------
        filter : str
            The filter for this query. See [Searchlight Query
            Language](https://developer.lockstep.io/docs/querying-with-searchlight)
        include : str
            To fetch additional data on this object, specify the list of
            elements to retrieve. Available collections: Invoice
        order : str
            The sort order for this query. See See [Searchlight Query
            Language](https://developer.lockstep.io/docs/querying-with-searchlight)
        pageSize : int
            The page size for results (default 200). See [Searchlight
            Query Language](https://developer.lockstep.io/docs/querying-with-searchlight)
        pageNumber : int
            The page number for results (default 0). See [Searchlight
            Query Language](https://developer.lockstep.io/docs/querying-with-searchlight)
        """
        path = "/api/v1/PaymentApplications/query"
        result = self.client.send_request("GET", path, None, {"filter": filter, "include": include, "order": order, "pageSize": pageSize, "pageNumber": pageNumber}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, FetchResult[PaymentAppliedModel](**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))
