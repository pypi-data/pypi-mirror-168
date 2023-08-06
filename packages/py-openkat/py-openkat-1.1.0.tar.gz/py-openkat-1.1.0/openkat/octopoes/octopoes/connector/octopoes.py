import json
from datetime import datetime
from typing import Optional, List, Type, Set, Union

import requests
from pydantic.tools import parse_obj_as
from requests import Response, HTTPError

from octopoes.api.models import Observation, Declaration, ServiceHealth
from octopoes.connector import RemoteException
from octopoes.models import Reference, OOI, ScanProfile, EmptyScanProfile, DeclaredScanProfile
from octopoes.models.exception import ObjectNotFoundException
from octopoes.models.origin import Origin, OriginType
from octopoes.models.tree import ReferenceTree, ReferenceNode
from octopoes.models.types import OOIType
from octopoes.models.ooi.network import Network


class OctopoesAPISession(requests.Session):
    def __init__(self, base_url: str, client: str):
        super().__init__()

        self._base_uri = f"{base_url}/{client}"

    @staticmethod
    def _verify_response(response: Response) -> None:
        try:
            response.raise_for_status()
        except HTTPError as error:
            if response.status_code == 404:
                data = response.json()
                raise ObjectNotFoundException(data["value"])
            if 500 <= response.status_code < 600:
                data = response.json()
                raise RemoteException(value=data["value"])
            raise error
        except json.decoder.JSONDecodeError:
            pass

    def request(
        self,
        method: str,
        url: Union[str, bytes],
        params: Optional[dict] = None,
        **kwargs,
    ) -> requests.Response:
        response = super().request(method, f"{self._base_uri}{url}", params, **kwargs)
        self._verify_response(response)
        return response


OBSERVATIONS = []
x = Network(name="internet")
DECLARATIONS = {"Network|internet": Declaration(ooi=Network(name="internet", scan_profile=DeclaredScanProfile(reference=x.reference, level=4)), valid_time=datetime.now())}


class OctopoesAPIConnector:

    """
    Methods on this Connector can throw
        - requests.exceptions.RequestException if HTTP connection to Octopoes API fails
        - connector.ObjectNotFoundException if the OOI node cannot be found
        - connector.RemoteException if an error occurs inside Octopoes API
    """

    def __init__(self, *args, **kwargs):
        pass

    def health(self) -> ServiceHealth:
        return ServiceHealth(service="octopoes", healthy=True)

    def list(
        self,
        types: Set[Type[OOI]],
        valid_time: Optional[datetime] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> List[OOI]:
        oois = []
        refs = []

        for x in OBSERVATIONS:
            for y in x.result:
                if y.reference in refs:
                    continue

                refs.append(y.reference)
                oois.append(y)

        for x in DECLARATIONS.values():
            if x.ooi.reference in refs:
                continue

            refs.append(x.ooi.reference)
            oois.append(x.ooi)

        return oois

    def get(self, reference: Reference, valid_time: Optional[datetime] = None) -> OOI:
        if reference in DECLARATIONS:
            return DECLARATIONS[reference].ooi

        for x in OBSERVATIONS:
            for y in x.result:
                if y.reference == reference:
                    return y

    def get_tree(
        self,
        reference: Reference,
        types: Optional[Set] = None,
        depth: Optional[int] = 1,
        valid_time: Optional[datetime] = None,
    ) -> ReferenceTree:
        if not types:
            types = set()

        return ReferenceTree(
            root=ReferenceNode(reference=reference, children={}),
            store={str(ooi.reference): ooi for ooi in self.list(types, valid_time=valid_time)},
        )

    def list_origins(self, reference: Reference, valid_time: Optional[datetime] = None) -> List[Origin]:
        origins = []
        for x in OBSERVATIONS:
            for y in x.result:
                if y.reference == reference:
                    origins.append(Origin(
                        origin_type=OriginType.OBSERVATION,
                        method=x.method,
                        source=x.source,
                        result=[ooi.reference for ooi in x.result],
                        task_id=x.task_id,
                    ))
                    break

        if reference in DECLARATIONS:
            x = DECLARATIONS[reference]

            origins.append(Origin(
                origin_type=OriginType.DECLARATION,
                method="manual",
                source=x.ooi.reference,
                result=[x.ooi.reference],
            ))

        return origins

    def save_observation(self, observation: Observation) -> None:
        for x in observation.result:
            sp = DeclaredScanProfile(reference=x.reference, level=0)  # Manually update scan profiles for now
            x.scan_profile = sp

        OBSERVATIONS.append(observation)

    def save_declaration(self, declaration: Declaration) -> None:
        sp = DeclaredScanProfile(reference=declaration.ooi.reference, level=4)
        declaration.ooi.scan_profile = sp

        DECLARATIONS[declaration.ooi.reference] = declaration

    def save_scan_profile(self, scan_profile: ScanProfile, valid_time: datetime):
        ooi = self.get(scan_profile.reference, valid_time)
        ooi.scan_profile = scan_profile

    def delete(self, reference: Reference, valid_time: Optional[datetime] = None) -> None:
        if reference in DECLARATIONS:
            del DECLARATIONS[reference]

        for x in OBSERVATIONS:
            new = []

            for y in x.result:
                if y.reference != reference:
                    new.append(y)

            x.result = new


# todo: use request Session and set default headers (accept-content, etc.)
class OctopoesAPIConnectorV1:

    """
    Methods on this Connector can throw
        - requests.exceptions.RequestException if HTTP connection to Octopoes API fails
        - connector.ObjectNotFoundException if the OOI node cannot be found
        - connector.RemoteException if an error occurs inside Octopoes API
    """

    def __init__(self, base_uri: str, client: str):
        self.session = OctopoesAPISession(base_uri, client)

    def health(self) -> ServiceHealth:
        return ServiceHealth.parse_obj(self.session.get(f"/health").json())

    def list(
        self,
        types: Set[Type[OOI]],
        valid_time: Optional[datetime] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> List[OOI]:
        params = {
            "types": [t.__name__ for t in types],
            "valid_time": valid_time,
            "offset": offset,
            "limit": limit,
        }
        res = self.session.get("/objects", params=params)
        return parse_obj_as(List[OOIType], res.json())

    def get(self, reference: Reference, valid_time: Optional[datetime] = None) -> OOI:
        res = self.session.get(
            "/object",
            params={"reference": str(reference), "valid_time": valid_time},
        )
        return parse_obj_as(OOIType, res.json())

    def get_tree(
        self,
        reference: Reference,
        types: Optional[Set] = None,
        depth: Optional[int] = 1,
        valid_time: Optional[datetime] = None,
    ) -> ReferenceTree:
        if types is None:
            types = set()
        res = self.session.get(
            "/tree",
            params={
                "reference": str(reference),
                "types": [t.__name__ for t in types],
                "depth": depth,
                "valid_time": valid_time,
            },
        )
        return ReferenceTree.parse_obj(res.json())

    def list_origins(self, reference: Reference, valid_time: Optional[datetime] = None) -> List[Origin]:
        params = {"reference": str(reference), "valid_time": valid_time}
        res = self.session.get("/origins", params=params)
        return parse_obj_as(List[Origin], res.json())

    def save_observation(self, observation: Observation) -> None:
        self.session.post("/observations", data=observation.json())

    def save_declaration(self, declaration: Declaration) -> None:
        self.session.post("/declarations", data=declaration.json())

    def save_scan_profile(self, scan_profile: ScanProfile, valid_time: datetime):
        params = {"valid_time": str(valid_time)}
        self.session.put("/scan_profiles", params=params, data=scan_profile.json())

    def delete(self, reference: Reference, valid_time: Optional[datetime] = None) -> None:
        params = {"reference": str(reference), "valid_time": valid_time}
        self.session.delete("/", params=params)
