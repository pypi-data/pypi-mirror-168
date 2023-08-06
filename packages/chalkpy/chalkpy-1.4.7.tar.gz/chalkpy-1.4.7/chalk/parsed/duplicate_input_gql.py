from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertFeatureIdGQL:
    fqn: str
    name: str
    namespace: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertReferencePathComponentGQL:
    parent: UpsertFeatureIdGQL
    child: UpsertFeatureIdGQL
    parent_to_child_attribute_name: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertFilterGQL:
    lhs: UpsertFeatureIdGQL
    op: str
    rhs: UpsertFeatureIdGQL


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertDataFrameGQL:
    columns: Optional[List[UpsertFeatureIdGQL]] = None
    filters: Optional[List[UpsertFilterGQL]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertFeatureReferenceGQL:
    underlying: UpsertFeatureIdGQL
    path: Optional[List[UpsertReferencePathComponentGQL]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertHasOneKindGQL:
    join: UpsertFilterGQL


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertHasManyKindGQL:
    join: UpsertFilterGQL
    columns: Optional[List[UpsertFeatureIdGQL]] = None
    filters: Optional[List[UpsertFilterGQL]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertScalarKindGQL:
    scalar_kind: str
    primary: bool
    base_classes: List[str]
    version: Optional[int]
    has_encoder_and_decoder: bool = False


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertFeatureTimeKindGQL:
    format: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertFeatureGQL:
    id: UpsertFeatureIdGQL

    scalar_kind: Optional[UpsertScalarKindGQL] = None
    has_many_kind: Optional[UpsertHasManyKindGQL] = None
    has_one_kind: Optional[UpsertHasOneKindGQL] = None
    feature_time_kind: Optional[UpsertFeatureTimeKindGQL] = None

    etl_offline_to_online: bool = False
    tags: Optional[List[str]] = None
    max_staleness: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class KafkaConsumerConfigGQL:
    broker: List[str]
    topic: List[str]
    ssl_keystore_location: Optional[str]
    client_id_prefix: Optional[str]
    group_id_prefix: Optional[str]
    topic_metadata_refresh_interval_ms: Optional[int]
    security_protocol: Optional[str]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertStreamResolverGQL:
    fqn: str
    kind: str
    function_definition: str
    config: KafkaConsumerConfigGQL
    environment: Optional[List[str]] = None
    doc: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertResolverOutputGQL:
    features: Optional[List[UpsertFeatureIdGQL]] = None
    dataframes: Optional[List[UpsertDataFrameGQL]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertResolverGQL:
    fqn: str
    kind: str
    function_definition: str
    output: UpsertResolverOutputGQL
    environment: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    doc: Optional[str] = None
    cron: Optional[str] = None
    inputs: Optional[List[UpsertFeatureReferenceGQL]] = None
    machine_type: Optional[str] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertSinkResolverGQL:
    fqn: str
    function_definition: str
    environment: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    doc: Optional[str] = None
    inputs: Optional[List[UpsertFeatureReferenceGQL]] = None
    machine_type: Optional[str] = None
    buffer_size: Optional[int] = None
    debounce: Optional[str] = None
    max_delay: Optional[str] = None
    upsert: Optional[bool] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UpsertGraphGQL:
    resolvers: Optional[List[UpsertResolverGQL]] = None
    features: Optional[List[UpsertFeatureGQL]] = None
    streams: Optional[List[UpsertStreamResolverGQL]] = None
