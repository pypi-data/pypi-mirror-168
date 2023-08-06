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
from lockstep.models.companydetailsmodel import CompanyDetailsModel
from lockstep.models.companymodel import CompanyModel
from lockstep.models.customersummarymodel import CustomerSummaryModel
from lockstep.models.vendorsummarymodel import VendorSummaryModel

class CompaniesClient:
    """
    API methods related to Companies
    """
    from lockstep.lockstep_api import LockstepApi

    def __init__(self, client: LockstepApi):
        self.client = client

    def retrieve_company(self, id: str, include: str) -> LockstepResponse[CompanyModel]:
        """
        Retrieves the Company specified by this unique identifier,
        optionally including nested data sets.

        A Company represents a customer, a vendor, or a company within
        the organization of the account holder. Companies can have
        parents and children, representing an organizational hierarchy
        of corporate entities. You can use Companies to track projects
        and financial data under this Company label.

        See [Vendors, Customers, and
        Companies](https://developer.lockstep.io/docs/companies-customers-and-vendors)
        for more information.

        Parameters
        ----------
        id : str
            The unique Lockstep Platform ID number of this Company; NOT
            the customer's ERP key
        include : str
            To fetch additional data on this object, specify the list of
            elements to retrieve. Available collections: Attachments,
            Contacts, CustomFields, Invoices, Notes, Classification
        """
        path = f"/api/v1/Companies/{id}"
        result = self.client.send_request("GET", path, None, {"include": include}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, CompanyModel(**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def update_company(self, id: str, body: object) -> LockstepResponse[CompanyModel]:
        """
        Updates a Company that matches the specified id with the
        requested information.

        The PATCH method allows you to change specific values on the
        object while leaving other values alone. As input you should
        supply a list of field names and new values. If you do not
        provide the name of a field, that field will remain unchanged.
        This allows you to ensure that you are only updating the
        specific fields desired.

        A Company represents a customer, a vendor, or a company within
        the organization of the account holder. Companies can have
        parents and children, representing an organizational hierarchy
        of corporate entities. You can use Companies to track projects
        and financial data under this Company label.

        See [Vendors, Customers, and
        Companies](https://developer.lockstep.io/docs/companies-customers-and-vendors)
        for more information.

        Parameters
        ----------
        id : str
            The unique Lockstep Platform ID number of this Company; NOT
            the customer's ERP key
        body : object
            A list of changes to apply to this Company
        """
        path = f"/api/v1/Companies/{id}"
        result = self.client.send_request("PATCH", path, body, {}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, CompanyModel(**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def disable_company(self, id: str) -> LockstepResponse[ActionResultModel]:
        """
        Disable the Company referred to by this unique identifier.

        A Company represents a customer, a vendor, or a company within
        the organization of the account holder. Companies can have
        parents and children, representing an organizational hierarchy
        of corporate entities. You can use Companies to track projects
        and financial data under this Company label.

        See [Vendors, Customers, and
        Companies](https://developer.lockstep.io/docs/companies-customers-and-vendors)
        for more information.

        Parameters
        ----------
        id : str
            The unique Lockstep Platform ID number of this Company; NOT
            the customer's ERP key
        """
        path = f"/api/v1/Companies/{id}"
        result = self.client.send_request("DELETE", path, None, {}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, ActionResultModel(**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def create_companies(self, body: list[CompanyModel]) -> LockstepResponse[list[CompanyModel]]:
        """
        Creates one or more Companies from a given model.

        A Company represents a customer, a vendor, or a company within
        the organization of the account holder. Companies can have
        parents and children, representing an organizational hierarchy
        of corporate entities. You can use Companies to track projects
        and financial data under this Company label.

        See [Vendors, Customers, and
        Companies](https://developer.lockstep.io/docs/companies-customers-and-vendors)
        for more information.

        Parameters
        ----------
        body : list[CompanyModel]
            The Companies to create
        """
        path = "/api/v1/Companies"
        result = self.client.send_request("POST", path, body, {}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, list[CompanyModel](**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def query_companies(self, filter: str, include: str, order: str, pageSize: int, pageNumber: int) -> LockstepResponse[FetchResult[CompanyModel]]:
        """
        Queries Companies for this account using the specified
        filtering, sorting, nested fetch, and pagination rules
        requested.

        More information on querying can be found on the [Searchlight
        Query Language](https://developer.lockstep.io/docs/querying-with-searchlight)
        page on the Lockstep Developer website.

        A Company represents a customer, a vendor, or a company within
        the organization of the account holder. Companies can have
        parents and children, representing an organizational hierarchy
        of corporate entities. You can use Companies to track projects
        and financial data under this Company label.

        See [Vendors, Customers, and
        Companies](https://developer.lockstep.io/docs/companies-customers-and-vendors)
        for more information.

        Parameters
        ----------
        filter : str
            The filter for this query. See [Searchlight Query
            Language](https://developer.lockstep.io/docs/querying-with-searchlight)
        include : str
            To fetch additional data on this object, specify the list of
            elements to retrieve. Available collections: Attachments,
            Contacts, CustomFields, Invoices, Notes, Classification
        order : str
            The sort order for the results, in the [Searchlight order
            syntax](https://github.com/tspence/csharp-searchlight).
        pageSize : int
            The page size for results (default 200, maximum of 10,000)
        pageNumber : int
            The page number for results (default 0)
        """
        path = "/api/v1/Companies/query"
        result = self.client.send_request("GET", path, None, {"filter": filter, "include": include, "order": order, "pageSize": pageSize, "pageNumber": pageNumber}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, FetchResult[CompanyModel](**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def query_customer_summary(self, filter: str, include: str, order: str, pageSize: int, pageNumber: int, reportDate: str) -> LockstepResponse[FetchResult[CustomerSummaryModel]]:
        """
        Queries Customer Summaries for this account using the specified
        filtering, sorting, nested fetch, and pagination rules
        requested.

        More information on querying can be found on the [Searchlight
        Query Language](https://developer.lockstep.io/docs/querying-with-searchlight)
        page on the Lockstep Developer website.

        The Customer Summary View represents a slightly different view
        of the data and includes some extra fields that might be useful.
        For more information, see the data format of the Customer
        Summary Model.

        See [Vendors, Customers, and
        Companies](https://developer.lockstep.io/docs/companies-customers-and-vendors)
        for more information.

        Parameters
        ----------
        filter : str
            The filter for this query. See [Searchlight Query
            Language](https://developer.lockstep.io/docs/querying-with-searchlight)
        include : str
            To fetch additional data on this object, specify the list of
            elements to retrieve. No collections are currently available
            but may be offered in the future
        order : str
            The sort order for the results, in the [Searchlight order
            syntax](https://github.com/tspence/csharp-searchlight).
        pageSize : int
            The page size for results (default 200, maximum of 10,000)
        pageNumber : int
            The page number for results (default 0)
        reportDate : str
            The date to calculate the fields on. If no date is entered
            the current UTC date will be used.
        """
        path = "/api/v1/Companies/views/customer-summary"
        result = self.client.send_request("GET", path, None, {"filter": filter, "include": include, "order": order, "pageSize": pageSize, "pageNumber": pageNumber, "reportDate": reportDate}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, FetchResult[CustomerSummaryModel](**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def query_vendor_summary(self, filter: str, include: str, order: str, pageSize: int, pageNumber: int, reportDate: str) -> LockstepResponse[FetchResult[VendorSummaryModel]]:
        """
        Queries Vendor Summaries for this account using the specified
        filtering, sorting, nested fetch, and pagination rules
        requested.

        More information on querying can be found on the [Searchlight
        Query Language](https://developer.lockstep.io/docs/querying-with-searchlight)
        page on the Lockstep Developer website.

        The Vendor Summary View represents a slightly different view of
        the data and includes some extra fields that might be useful.
        For more information, see the data format of the Vendor Summary
        Model.

        See [Vendors, Customers, and
        Companies](https://developer.lockstep.io/docs/companies-customers-and-vendors)
        for more information.

        Parameters
        ----------
        filter : str
            The filter for this query. See [Searchlight Query
            Language](https://developer.lockstep.io/docs/querying-with-searchlight)
        include : str
            To fetch additional data on this object, specify the list of
            elements to retrieve. No collections are currently available
            but may be offered in the future
        order : str
            The sort order for the results, in the [Searchlight order
            syntax](https://github.com/tspence/csharp-searchlight).
        pageSize : int
            The page size for results (default 200, maximum of 10,000)
        pageNumber : int
            The page number for results (default 0)
        reportDate : str
            The date to calculate the fields on. If no date is entered
            the current UTC date will be used.
        """
        path = "/api/v1/Companies/views/vendor-summary"
        result = self.client.send_request("GET", path, None, {"filter": filter, "include": include, "order": order, "pageSize": pageSize, "pageNumber": pageNumber, "reportDate": reportDate}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, FetchResult[VendorSummaryModel](**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def retrieve_company_detail(self, id: str) -> LockstepResponse[CompanyDetailsModel]:
        """
        Retrieves the Company Details specified by this unique
        identifier, optionally including nested data sets.

        The Company Detail View represents a slightly different view of
        the data and includes some extra fields that might be useful.
        For more information, see the data format of the Company Detail
        Model.

        See [Vendors, Customers, and
        Companies](https://developer.lockstep.io/docs/companies-customers-and-vendors)
        for more information.

        Parameters
        ----------
        id : str
            The unique Lockstep Platform ID number of this Company; NOT
            the company's ERP key
        """
        path = f"/api/v1/Companies/views/details/{id}"
        result = self.client.send_request("GET", path, None, {}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, CompanyDetailsModel(**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def set_company_logo(self, id: str, filename: str) -> LockstepResponse[CompanyModel]:
        """
        Sets the logo for specified company. The logo will be stored in
        the Lockstep Platform and will be **publicly accessible**.

        .jpg, .jpeg, and .png are supported. 5MB maximum. If no logo is
        uploaded, the existing logo will be deleted.

        A Company represents a customer, a vendor, or a company within
        the organization of the account holder. Companies can have
        parents and children, representing an organizational hierarchy
        of corporate entities. You can use Companies to track projects
        and financial data under this Company label.

        See [Vendors, Customers, and
        Companies](https://developer.lockstep.io/docs/companies-customers-and-vendors)
        for more information.

        Parameters
        ----------
        id : str
            The unique Lockstep Platform ID number of this Company; NOT
            the customer's ERP key
        filename : str
            The full path of a file to upload to the API
        """
        path = f"/api/v1/Companies/{id}/logo"
        result = self.client.send_request("POST", path, None, {}, filename)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, CompanyModel(**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))
