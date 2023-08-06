from http import HTTPStatus
from typing import List

from pydantic import parse_obj_as

from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.v2.schema.baseline import Baseline
from fiddler.v2.utils.exceptions import handle_api_error_response
from fiddler.v2.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)

logger = logging.getLogger(__name__)


class BaselineMixin:
    client: RequestClient
    organization_name: str

    @handle_api_error_response
    def get_baselines(
        self, project_name: str, model_name: str = None
    ) -> List[Baseline]:
        """Get list of all Baselines at project or model level

        :params project_name: project to list baselines from
        :params model_name: [Optional] model within project to list baselines from
        :returns: List containing Baseline objects
        """
        response = self.client.get(
            url='baselines/',
            params={
                'organization_name': self.organization_name,
                'project_name': project_name,
                'model_name': model_name,
            },
        )
        _, items = PaginatedResponseHandler(response).get_pagination_details_and_items()
        return parse_obj_as(List[Baseline], items)

    @handle_api_error_response
    def get_baseline(self, project_name: str, baseline_name: str) -> Baseline:
        """Get the details of a Baseline.

        :params project_name: The project to which the Baseline belongs to
        :params baseline_name: The Baseline name of which you need the details
        :returns: Baseline object which contains the details
        """
        response = self.client.get(
            url=f'baselines/{self.organization_name}:{project_name}:{baseline_name}',
        )
        response_handler = APIResponseHandler(response)
        return Baseline.deserialize(response_handler)

    @handle_api_error_response
    def add_baseline(
        self,
        project_name: str,
        name: str,
        type: str,
        model_association: str = None,
        dataset_name: str = None,
        model_name: str = None,
        start_time: int = None,
        end_time: int = None,
        offset: int = None,
        window_size: int = None,
    ) -> Baseline:
        """Function to add a Baseline to fiddler for monitoring

        :param project_name: project name where the Baseline will be added
        :type project_name: string
        :param name: name of the Baseline
        :type name: string
        :param type: type (DATASET, RELATIVE, STATIC) of the Baseline
        :type type: string
        :param model_association: (optional) model to associate baseline to
        :type model_association: string
        :param dataset_name: (optional) dataset to be used as baseline
        :type dataset_name: string
        :param model_name: (optional) model to be used as baseline
        :type model_name: string
        :param start_time: (optional) milliseconds since epoch to be used as start time for STATIC baseline
        :type start_time: int
        :param end_time: (optional) milliseconds since epoch to be used as end time for STATIC baseline
        :type end_time: int
        :param offset: (optional) seconds from current time to be used for RELATIVE baseline
        :type offset: int
        :param window_size: (optional) width of window in seconds to be used for RELATIVE baseline
        :type window_size: int

        :return: Baseline object which contains the Baseline details
        """

        request_body = Baseline(
            organization_name=self.organization_name,
            project_name=project_name,
            name=name,
            type=type,
            model_association=model_association,
            dataset_name=dataset_name,
            model_name=model_name,
            start_time=start_time,
            end_time=end_time,
            offset=offset,
            window_size=window_size,
        ).dict()

        if 'id' in request_body:
            request_body.pop('id')

        response = self.client.post(
            url='baselines/',
            data=request_body,
        )

        if response.status_code == HTTPStatus.OK:
            logger.info(f'{name} setup successful')
            return Baseline.deserialize(APIResponseHandler(response))

    @handle_api_error_response
    def delete_baseline(self, project_name: str, baseline_name: str) -> None:
        """Delete a Baseline

        :params project_name: Project name to which the Baseline belongs to.
        :params Baseline_name: Baseline name to be deleted

        :returns: None
        """
        response = self.client.delete(
            url=f'baselines/{self.organization_name}:{project_name}:{baseline_name}',
        )
        if response.status_code == HTTPStatus.OK:
            logger.info(f'{baseline_name} delete request received.')
        else:
            # @TODO: Handle non 200 status response
            logger.info('Delete unsuccessful')

    @handle_api_error_response
    def attach_baseline(
        self,
        project_name: str,
        name: str,
        model: str,
    ) -> None:
        """Function to add a Baseline to fiddler for monitoring

        :param project_name: project name where the Baseline will be added
        :type project_name: string
        :param name: name of the Baseline
        :type name: string
        :param model_association: (optional) model to associate baseline to
        :type model_association: string
        """

        response = self.client.post(
            url=f'baselines/{self.organization_name}:{project_name}:{name}:{model}',
            data={},
        )

        if APIResponseHandler(response).get_status_code() != HTTPStatus.OK:
            logger.info(f'Baseline {name} attachment to model {model} failed')
        else:
            logger.info(f'Baseline {name} successfully attached to model {model}')

    @handle_api_error_response
    def detach_baseline(
        self,
        project_name: str,
        name: str,
        model: str,
    ) -> None:
        """Function to remove baseline from model

        :param project_name: project name where the Baseline will be added
        :type project_name: string
        :param name: name of the Baseline
        :type name: string
        :param model: (optional) model to associate baseline to
        :type model: string
        """

        response = self.client.delete(
            url=f'baselines/{self.organization_name}:{project_name}:{name}:{model}',
            data={},
        )

        if APIResponseHandler(response).get_status_code() != HTTPStatus.OK:
            logger.info(f'Baseline {name} detachment from model {model} failed')
        else:
            logger.info(f'Baseline {name} successfully detached from model {model}')
