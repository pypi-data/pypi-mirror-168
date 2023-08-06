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
from lockstep.models.activitymodel import ActivityModel
from lockstep.models.activitystreamitemmodel import ActivityStreamItemModel

class ActivitiesClient:
    """
    API methods related to Activities
    """
    from lockstep.lockstep_api import LockstepApi

    def __init__(self, client: LockstepApi):
        self.client = client

    def retrieve_activity(self, id: str, include: str) -> LockstepResponse[ActivityModel]:
        """
        Retrieves the Activity specified by this unique identifier,
        optionally including nested data sets.

        An Activity contains information about work being done on a
        specific accounting task. You can use Activities to track
        information about who has been assigned a specific task, the
        current status of the task, the name and description given for
        the particular task, the priority of the task, and any amounts
        collected, paid, or credited for the task.

        Parameters
        ----------
        id : str
            The unique Lockstep Platform ID number of this Activity
        include : str
            To fetch additional data on this object, specify the list of
            elements to retrieve. Available collections: Company,
            Attachments, CustomFields, Notes, References, and
            UserAssignedToName
        """
        path = f"/api/v1/Activities/{id}"
        result = self.client.send_request("GET", path, None, {"include": include}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, ActivityModel(**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def update_activity(self, id: str, body: object) -> LockstepResponse[ActivityModel]:
        """
        Updates an activity that matches the specified id with the
        requested information.

        The PATCH method allows you to change specific values on the
        object while leaving other values alone. As input you should
        supply a list of field names and new values. If you do not
        provide the name of a field, that field will remain unchanged.
        This allows you to ensure that you are only updating the
        specific fields desired.

        An Activity contains information about work being done on a
        specific accounting task. You can use Activities to track
        information about who has been assigned a specific task, the
        current status of the task, the name and description given for
        the particular task, the priority of the task, and any amounts
        collected, paid, or credited for the task.

        Parameters
        ----------
        id : str
            The unique Lockstep Platform ID number of the Activity to
            update
        body : object
            A list of changes to apply to this Activity
        """
        path = f"/api/v1/Activities/{id}"
        result = self.client.send_request("PATCH", path, body, {}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, ActivityModel(**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def delete_activity(self, id: str) -> LockstepResponse[ActivityModel]:
        """
        Delete the Activity referred to by this unique identifier.

        An Activity contains information about work being done on a
        specific accounting task. You can use Activities to track
        information about who has been assigned a specific task, the
        current status of the task, the name and description given for
        the particular task, the priority of the task, and any amounts
        collected, paid, or credited for the task.

        Parameters
        ----------
        id : str
            The unique Lockstep Platform ID number of the Activity to
            delete
        """
        path = f"/api/v1/Activities/{id}"
        result = self.client.send_request("DELETE", path, None, {}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, ActivityModel(**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def create_activities(self, body: list[ActivityModel]) -> LockstepResponse[list[ActivityModel]]:
        """
        Creates one or more activities from a given model.

        An Activity contains information about work being done on a
        specific accounting task. You can use Activities to track
        information about who has been assigned a specific task, the
        current status of the task, the name and description given for
        the particular task, the priority of the task, and any amounts
        collected, paid, or credited for the task.

        Parameters
        ----------
        body : list[ActivityModel]
            The Activities to create
        """
        path = "/api/v1/Activities"
        result = self.client.send_request("POST", path, body, {}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, list[ActivityModel](**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def query_activities(self, filter: str, include: str, order: str, pageSize: int, pageNumber: int) -> LockstepResponse[FetchResult[ActivityModel]]:
        """
        Queries Activities for this account using the specified
        filtering, sorting, nested fetch, and pagination rules
        requested.

        More information on querying can be found on the [Searchlight
        Query Language](https://developer.lockstep.io/docs/querying-with-searchlight)
        page on the Lockstep Developer website.

        An Activity contains information about work being done on a
        specific accounting task. You can use Activities to track
        information about who has been assigned a specific task, the
        current status of the task, the name and description given for
        the particular task, the priority of the task, and any amounts
        collected, paid, or credited for the task.

        Parameters
        ----------
        filter : str
            The filter for this query. See [Searchlight Query
            Language](https://developer.lockstep.io/docs/querying-with-searchlight)
        include : str
            To fetch additional data on this object, specify the list of
            elements to retrieve. Available collections: Company,
            Attachments, CustomFields, Notes, References, and
            UserAssignedToName
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
        path = "/api/v1/Activities/query"
        result = self.client.send_request("GET", path, None, {"filter": filter, "include": include, "order": order, "pageSize": pageSize, "pageNumber": pageNumber}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, FetchResult[ActivityModel](**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def retrieve_activity_stream(self, id: str) -> LockstepResponse[list[ActivityStreamItemModel]]:
        """
        Retrieves a list of items representing the activity stream for
        the supplied activity id.

        An Activity contains information about work being done on a
        specific accounting task. You can use Activities to track
        information about who has been assigned a specific task, the
        current status of the task, the name and description given for
        the particular task, the priority of the task, and any amounts
        collected, paid, or credited for the task.

        Parameters
        ----------
        id : str
            The unique Lockstep Platform ID number of this Activity
        """
        path = f"/api/v1/Activities/{id}/stream"
        result = self.client.send_request("GET", path, None, {}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, list[ActivityStreamItemModel](**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))

    def forward_activity(self, activityId: str, userId: str) -> LockstepResponse[ActivityModel]:
        """
        Forwards an activity by creating a new activity with all child
        references and assigning the new activity to a new user.

        An Activity contains information about work being done on a
        specific accounting task. You can use Activities to track
        information about who has been assigned a specific task, the
        current status of the task, the name and description given for
        the particular task, the priority of the task, and any amounts
        collected, paid, or credited for the task.

        Parameters
        ----------
        activityId : str

        userId : str

        """
        path = f"/api/v1/Activities/{activityId}/forward/{userId}"
        result = self.client.send_request("POST", path, None, {}, None)
        if result.status_code >= 200 and result.status_code < 300:
            return LockstepResponse(True, result.status_code, ActivityModel(**result.json()), None)
        else:
            return LockstepResponse(False, result.status_code, None, ErrorResult(**result.json()))
