from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, EmailStr, validator

#
# GENERIC
#


class CustomError(BaseModel):
    message: str
    reasons: List[str]


#
# HTTP
#


class HttpSuccess(BaseModel):
    ok: str


class HttpError(BaseModel):
    status_code: int
    error: CustomError


#
# JWT
#


class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"


class JwtParam(BaseModel):
    email: EmailStr
    first_name: str
    role: RoleEnum


#
# FEATURE REQUEST
#


class StatusEnum(str, Enum):
    created = "created"
    accepted = "accepted"
    wip = "wip"
    implemented = "implemented"
    rejected = "rejected"


class TypeEnum(str, Enum):
    feature = "feature"
    bug = "bug"


class FeatureRequest(BaseModel):
    uuid: Optional[str]
    title: str
    type: TypeEnum
    description: str
    author: EmailStr
    status: StatusEnum


class FeatureRequestList(BaseModel):
    __root__: List[FeatureRequest]


class FeatureRequestMeta(BaseModel):
    uuid: str
    upvote_count: int
    current_user_voted: bool


class FeatureRequestMetaList(BaseModel):
    __root__: List[FeatureRequestMeta]


########### DEPOXY


class Database(BaseModel):
    databaseEid: str
    databaseName: str
    description: str
    createTime: str
    catalogId: str

    # @validator('createTime')
    # def create_time_iso_8601(cls, v: str):
    #    ...


class Databases(BaseModel):
    __root__: List[Database]


class Column(BaseModel):
    name: str
    type: str
    comment: str


class SerdeInfo(BaseModel):
    serializationLibrary: str
    parameters: Dict


class StorageDescriptor(BaseModel):
    location: str
    inputFormat: str
    outputFormat: str
    isCompressed: bool
    numberOfBuckets: int
    bucketColumns: List
    sortColumns: List
    parameters: Dict
    isStoredAsSubDirectories: bool


class PartitionKey(BaseModel):
    name: str
    type: str
    comment: str


class GeneralInfo(BaseModel):
    tableEid: str
    tableName: str
    databaseName: str
    createTime: str  # TODO: validator
    updateTime: str  # TODO: validator
    tableType: str
    createdBy: str
    versionId: str
    catalogId: str
    isRegisteredWithLakeFormation: bool


class TableDetail(BaseModel):
    generalInfo: GeneralInfo
    storageDescriptor: StorageDescriptor
    serdeInfo: SerdeInfo
    partitionKeys: List[PartitionKey]
    columns: List[Column]


class TableDetails(BaseModel):
    __root__: List[TableDetail]


class TableSummary(BaseModel):
    tableEid: str
    tableName: str
    databaseEid: str
    databaseName: str
    createTime: str  # TODO: validator
    updateTime: str  # TODO: validator
    location: str


class TableSummaries(BaseModel):
    __root__: List[TableSummary]


#######################


class QuerySummary(BaseModel):
    queryExecutionId: str
    queryState: str
    queryStart: str  # TODO: validator
    queryRunTimeMs: int
    queryDataScanned: int


class QuerySummaries(BaseModel):
    __root__: List[QuerySummary]


class Statistics(BaseModel):
    engineExecutionTime: int
    dataScannedInBytes: int
    totalExecutionTime: int
    queryQueueTime: int
    queryPlanningTime: Optional[int]
    serviceProcessingTime: int


class QueryDetail(BaseModel):
    queryExecutionId: str
    query: str
    statementType: str
    outputLocation: Optional[str]
    encryptionOption: Optional[str]
    kmsKey: Optional[str]
    database: str
    catalog: str
    status: str
    submissionDate: str  # TODO: validator
    completionDate: Optional[str]  # TODO: validator
    errorMessage: Optional[str]
    workGroup: str
    statistics: Statistics


#############################


class JobSummary(BaseModel):
    jobEid: str
    jobName: str
    lastJobRunState: Optional[str]
    lastStartedOn: Optional[str]
    lastCompletedOn: Optional[str]
    lastExecutionTime: Optional[int]


class JobSummaries(BaseModel):
    __root__: List[JobSummary]


class Command(BaseModel):
    name: str
    scriptLocation: str
    pythonVersion: str


class JobDetail(BaseModel):
    jobEid: str
    jobName: str
    description: str
    role: str
    createdOn: str
    lastModifiedOn: str
    glueVersion: str
    maxRetries: int
    allocatedCapacity: int
    maxCapacity: int
    timeout: int
    workerType: Optional[str]
    numberOfWorkers: Optional[int]
    command: Optional[Command]
    defaultArguments: Optional[Dict]
    lastJobRunState: Optional[str]
    lastStartedOn: Optional[str]
    lastCompletedOn: Optional[str]
    lastExecutionTime: Optional[int]


class JobRun(BaseModel):
    jobRunAwsId: str
    jobName: str
    jobEid: str
    triggerName: Optional[str]
    jobRunState: str
    startedOn: str  # TODO: validator
    completedOn: str  # TODO: validator
    executionTime: int
    errorMessage: Optional[str]


class JobRuns(BaseModel):
    __root__: List[JobRun]


class JobTrigger(BaseModel):
    triggerName: str
    triggerType: str
    triggerState: str
    triggerSchedule: str


class JobTriggers(BaseModel):
    __root__: List[JobTrigger]


##########################


class TableMeta(BaseModel):
    databaseName: str
    tableName: str
    sizeIecMiB: float
    fileCount: int


class TableMetaList(BaseModel):
    __root__: List[TableMeta]


class TableTreemap(BaseModel):
    tableName: str
    sizeIecMiB: float
    fileCount: int


class DatabaseTreemap(BaseModel):
    databaseName: str
    tables: List[TableTreemap]


class TablesTreemap(BaseModel):
    __root__: List[DatabaseTreemap]


################ cache


class EidCache(BaseModel):
    forward_dict: Dict[str, str]
    reverse_dict: Dict[str, str]
    created_at: Optional[str]
    request_count: int = 0


class JobSummariesCache(BaseModel):
    job_summaries: JobSummaries
    created_at: Optional[str]
    request_count: int = 0


class TableSummariesCache(BaseModel):
    table_summaries: TableSummaries
    created_at: Optional[str]
    request_count: int = 0


class QuerySummariesCache(BaseModel):
    query_summaries: QuerySummaries
    created_at: Optional[str]
    request_count: int = 0
