from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.dataset import Dataset
from ...models.forbidden_error import ForbiddenError
from ...models.not_found_error import NotFoundError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    dataset_id: str,
) -> Dict[str, Any]:
    url = "{}/datasets/{dataset_id}".format(client.base_url, dataset_id=dataset_id)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Dataset, ForbiddenError, NotFoundError]]:
    if response.status_code == 200:
        response_200 = Dataset.from_dict(response.json())

        return response_200
    if response.status_code == 403:
        response_403 = ForbiddenError.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = NotFoundError.from_dict(response.json())

        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Dataset, ForbiddenError, NotFoundError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    dataset_id: str,
) -> Response[Union[Dataset, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        dataset_id=dataset_id,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    dataset_id: str,
) -> Optional[Union[Dataset, ForbiddenError, NotFoundError]]:
    """Get a dataset, which is a tabular data construct that stores typed columns and rows of data. Call this endpoint to download it as a CSV file. It returns an S3 URL, from which you can download the file."""

    return sync_detailed(
        client=client,
        dataset_id=dataset_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    dataset_id: str,
) -> Response[Union[Dataset, ForbiddenError, NotFoundError]]:
    kwargs = _get_kwargs(
        client=client,
        dataset_id=dataset_id,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    dataset_id: str,
) -> Optional[Union[Dataset, ForbiddenError, NotFoundError]]:
    """Get a dataset, which is a tabular data construct that stores typed columns and rows of data. Call this endpoint to download it as a CSV file. It returns an S3 URL, from which you can download the file."""

    return (
        await asyncio_detailed(
            client=client,
            dataset_id=dataset_id,
        )
    ).parsed
